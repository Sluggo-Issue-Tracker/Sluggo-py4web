# quick and dirty moving the helper functions to their own class because our imports
# were getting way too long

from datetime import datetime, timezone
import json
from . common import db, Field, auth
import pathlib

class Helper:

    @staticmethod
    def get_user_email():
        return auth.current_user.get('email') if auth.current_user else None

    @staticmethod
    def get_user_title():
        return auth.current_user.get('first_name') + " " + auth.current_user.get(
            'last_name') if auth.current_user else None

    @staticmethod
    def get_user_name(entry):
        r = db(db.auth_user.email == entry.get("user_email")).select().first()
        return r.first_name + " " + r.last_name if r is not None else "Unknown"

    @staticmethod
    def get_user_and_id(entry):
        r = db(db.auth_user.email == entry.get("user_email")).select(db.auth_user.id, db.auth_user.email).first()
        return {
            'user_id': r.id,
            'user_name': r.first_name + " " + r.last_name if r is not None else "Unknown"
        }

    @staticmethod
    def get_user():
        return auth.current_user.get('id') if auth.current_user else None

    @staticmethod
    def get_role():
        user = db(db.users.user == Helper.get_user()).select().first()
        return user.role.capitalize() if user is not None else "Unapproved"

    @staticmethod
    def get_users_by_tag_id(tag_list):
        if tag_list is None:
            return list()

        return db(db.user_tag.tag_id in tag_list).select(
            db.users.ALL, left=db.users.on(db.users.id == db.user_tag.user_id), groupby=db.users.id
        ).as_list()


    @staticmethod
    def get_time():
        return datetime.now(timezone.utc)

    @staticmethod
    def time_str():
        time = Helper.get_time()
        return time.strftime("%m/%d/%Y %H:%M:%S %Z")

    # MARK: Data transmission
    @staticmethod
    def safe_json_dumps(obj):
        # Obtained from https://stackoverflow.com/a/56138540
        # Attempt to run dumps and replace any non-compatible types
        # (probably not needed in JS)
        default = lambda obj: f"<<non-serializable: {type(obj).__qualname__}>>"
        return json.dumps(obj, default=default, skipkeys=True)

    @staticmethod
    def get_tags_list():
        tags = db(db.global_tag).select().as_list()
        list = []
        for tag in tags:
            list.append(tag.get('tag_name').capitalize())
        return list

    @staticmethod
    def get_tags_list_approved():
        tags = db(db.global_tag.approved == True).select().as_list()
        list = []
        for tag in tags:
            list.append(tag.get('tag_name').capitalize())
        return list

    @staticmethod
    def get_user_tag_by_name(user):
        tags = db(db.user_tag.user_id == user.get('id')).select(db.global_tag.ALL, left=db.global_tag.on(
            db.global_tag.id == db.user_tag.tag_id))
        list = []
        for tag in tags:
            if tag.get('approved'):
                list.append(tag.get('tag_name').capitalize())
        return list

    @staticmethod
    def get_web_tag_list_for_user_id(user_id):
        tagRels = db(db.user_tag.user_id == user_id).select().as_list()
        tags = []
        for tagRel in tagRels:
            # Find the corresponding tag
            foundTag = db((db.global_tag.id == tagRel["tag_id"]) & (db.global_tag.approved == True)).select().first()
            if foundTag:
                tags.append(foundTag)

        webTagPairs = []

        for tag in tags:
            workingWebTag = dict()
            workingWebTag["tag_name"] = tag.tag_name
            workingWebTag["tag_id"] = tag.id

            webTagPairs.append(workingWebTag)

        return webTagPairs


    @staticmethod
    def get_ticket_tags_by_id(ticket_id):
        if ticket_id is None:
            return list()
        tags = db(db.ticket_tag.ticket_id == ticket_id).select \
            (db.global_tag.ALL,
             left=db.global_tag.on(db.global_tag.id == db.ticket_tag.tag_id))

        list = []
        for tag in tags:
            if tag.get('approved'):
                list.append(tag.as_dict())
        return list

    @staticmethod
    def get_sub_tickets_by_parent_id(parent_id):
        if parent_id is None:
            return None

        return db(db.sub_tickets.parent_id == parent_id).select \
            (db.tickets.ALL,
             left=db.tickets.on(db.tickets.id == db.sub_tickets.child_id)).as_list()

    @staticmethod
    def get_comment_thread_by_ticket_id():
        # TODO: implement this once we get the chance
        return None

    # MARK: Fetching tickets
    @staticmethod
    def get_tickets_for_ids(ticket_ids):
        return list(map(lambda x: db(db.tickets.id == x).select().as_list()[0], ticket_ids))

    @staticmethod
    def attach_tags_for_tickets(tickets):
        for ticket in tickets:
            # Fetch tags from rels
            fetchedRels = db(db.ticket_tag.ticket_id == ticket["id"]).select()
            tags = list(map(lambda rel: db(db.global_tag.id == rel.tag_id).select().first(), fetchedRels))
            if len(tags) == 0:
                ticket["tag_string"] = "No Tags"
                continue
            else:
                ticket["tag_string"] = ""
                for tag in tags:
                    ticket["tag_string"] = ticket["tag_string"] + tag.tag_name + " "

    # MARK: Pinning tickets

    @staticmethod
    def get_pinned_ticket_ids_for_user(given_user_id):
        # Assuming parameter is the auth.user object
        # Query for pinned tickets given user ID
        pinnedTicketsQuery = db(db.user_pins.auth_user_id == given_user_id).select().as_list()
        pinnedTickets = list(map(lambda x: x['ticket_id'], pinnedTicketsQuery))
        return pinnedTickets

    @staticmethod
    def cleanup_icon(row_id):
        ''' When adding new images, it will delete
            the old profile picture to not take up
            too much space on the filesystem.'''
        row = db(db.users.id == row_id).select().first()
        if row == None or row['icon'] == 'default.jpg':
            return

        img_name = row['icon']
        path = pathlib.Path(__file__).resolve().parent / 'static' / 'images' / 'profile_pics' / img_name
        if path.exists():
            path.unlink()

