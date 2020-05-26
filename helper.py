# quick and dirty moving the helper functions to their own class because our imports
# were getting way to fucking long

from datetime import datetime, timezone
from . common import db, Field, auth

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

    @staticmethod
    def get_tags_list():
        tags = db(db.global_tag).select().as_list()
        list = []
        for tag in tags:
            list.append(tag.get('tag_name').capitalize())
        return list

    @staticmethod
    def get_user_tag_by_name(user):
        tags = db(db.user_tag.user_id == user.get('id')).select(db.global_tag.tag_name, left=db.global_tag.on(
            db.global_tag.id == db.user_tag.tag_id))
        list = []
        for tag in tags:
            list.append(tag.get('tag_name').capitalize())
        return list

    @staticmethod
    def get_ticket_tags_by_id(ticket_id):
        if ticket_id is None:
            return list()

        return db(db.ticket_tag.ticket_id == ticket_id).select \
            (db.global_tag.ALL,
             left=db.global_tag.on(db.global_tag.id == db.ticket_tag.tag_id)).as_list()

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

