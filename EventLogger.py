from datetime import datetime, timezone
import json
from . common import db, Field, auth

class EventLogger:
    @staticmethod
    def log_comment(content, ticket_id, action_auth_user):
        db.events.insert(
            type="post-comment",
            description=content,
            related_ticket=ticket_id,
            action_user=action_auth_user
        )
        print("Logged comment by user " + str(action_auth_user) + " with message " + str(content) + " on ticket " +\
            str(ticket_id))

    @staticmethod
    def log_status_change(status, ticket_id, action_auth_user):
        db.events.insert(
            type="ticket-status-change",
            description=status,
            related_ticket=ticket_id,
            action_user=action_auth_user
        )
        print("Logged status change by user " + str(action_auth_user) + " with status " + str(status) + " on ticket " +\
            str(ticket_id))
    
    # @staticmethod
    # def get_recent_updates_for_user(user_id):
    #     return []