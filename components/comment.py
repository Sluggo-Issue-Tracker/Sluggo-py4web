"""
this component serves to provide comment functionality
"""

from py4web import action, URL, request
from yatl.helpers import XML
from py4web.utils.url_signer import URLSigner
from py4web.core import Fixture, HTTP
from ..EventLogger import EventLogger
from ..models import Helper


class Comment(Fixture):
    COMMENT = """<comment get_url="{get_url}" add_url="{add_url}"
    edit_url="{edit_url}" delete_url="{delete_url}" ticket_id="{ticket_id}"></comment>"""

    def __init__(self, url, session, signer=None, db=None, auth=None):
        self.get_url = url + '/get'
        self.add_url = url + '/add'
        self.edit_url = url + '/edit'
        self.delete_url = url + '/delete'
        self.signer = signer or URLSigner(session)
        self.db = db
        self.auth = auth

        # creates actions (entry points of the calls)
        # same as decorators but registered on object creation
        # very similar to Luca's old component creation
        self.__prerequisites__ = [session]
        args = list(filter(None, [session, db, auth, self.signer.verify()]))

        # function definition
        f = action.uses(*args)(self.get_comments)
        action(self.get_url + "/<id>", method=["GET"])(f)

        f = action.uses(*args)(self.add_comment)
        action(self.add_url, method=["POST"])(f)

        f = action.uses(*args)(self.edit_comment)
        action(self.edit_url, method=["POST"])(f)

        f = action.uses(*args)(self.delete_comment)
        action(self.delete_url, method=["POST"])(f)

    def __call__(self, id=None):
        # a clear cut interface is better than dependence on global variables, but including the same user
        # every time might make data strained, adding user as a prop may be added later
        return XML(Comment.COMMENT.format(
            get_url=URL(self.get_url, id, signer=self.signer),
            add_url=URL(self.add_url, signer=self.signer),
            edit_url=URL(self.edit_url, signer=self.signer),
            delete_url=URL(self.delete_url, signer=self.signer),
            ticket_id=id
        ))

    # retrieve all comments associated with this ticket
    def get_comments(self, id=None):
        if not id.isnumeric():
            raise HTTP(500)

        user_id = self.auth.current_user.get('id')

        # TODO: figure out if i want to attach image urls or have them load in a different call
        comments = self.db(self.db.comment.ticket_id == id).select(
            self.db.comment.ALL, self.db.auth_user.first_name, self.db.auth_user.last_name,
            left=self.db.auth_user.on(self.db.comment.user_id == self.db.auth_user.id)
        ).as_list()
        comments = list(map(lambda x: {**x["comment"], **x["auth_user"]}, comments))

        # fetch the full user
        user = self.db(self.db.users.user == user_id).select().first()

        for comment in comments:
            comment['editable'] = comment.get('user_id') == self.auth.current_user.get('id') or user.role == "admin"
            comment['img_url'] = Helper.get_user_icon(user["icon"])

        return dict(comments=comments)

    # insert a comment associated with this ticket
    # using post because it's way simpler to pass urls this way
    def add_comment(self):
        content = request.json.get('content')
        ticket_id = request.json.get('ticket_id')

        if not content or not ticket_id:
            raise HTTP(500)

        # inserting it manually because the default does not seem to work
        user_id = self.auth.current_user.get('id') if self.auth.current_user else None
        first_name = self.auth.current_user.get('first_name') if self.auth.current_user else None
        last_name = self.auth.current_user.get('last_name') if self.auth.current_user else None

        EventLogger.log_comment(content, ticket_id, user_id)

        return dict(id=self.db.comment.insert(ticket_id=ticket_id, content=content, user_id=user_id),
                    first_name=first_name, last_name=last_name)

    # edit a comment associated with this ticket
    # using post for ids
    def edit_comment(self):
        comment_id = request.json.get('comment_id')
        content = request.json.get('content')
        auth_user_id = self.auth.current_user.get('id') if self.auth.current_user else None

        if not content or not comment_id or not auth_user_id:
            raise HTTP(500)

        comment = self.db.comment[comment_id]
        user = self.db(self.db.users.user == auth_user_id).select().first()

        if comment.user_id != auth_user_id and user.role != "admin":
            raise HTTP(403)

        comment.update_record(content=content)
        return "ok"

    # delete a comment
    # using post for ids simple
    def delete_comment(self):
        comment_id = request.json.get('comment_id')
        auth_user_id = self.auth.current_user.get('id') if self.auth.current_user else None

        if not comment_id or not auth_user_id:
            raise HTTP(500)

        comment = self.db.comment[comment_id]
        user = self.db(self.db.users.user == auth_user_id).select().first()

        if comment.user_id != auth_user_id and user.role != "admin":
            raise HTTP(403)

        comment.delete_record()
        return "ok boomer"
