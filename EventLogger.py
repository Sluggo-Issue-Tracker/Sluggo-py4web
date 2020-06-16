# EventLogger.py - event logging system for Recent Updates pane
# part of Sluggo, a free and open source issue tracker
# Copyright (c) 2020 Slugbotics - see git repository history for individual committers
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from datetime import datetime, timezone
import json
from . common import db, Field, auth
from . helper import Helper

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
    
    @staticmethod
    def get_recent_updates_for_user(user_id):
        events = []

        # Get events pertaining to any pinned tickets
        pinned_ticket_ids = Helper.get_pinned_ticket_ids_for_user(user_id)
        for ptid in pinned_ticket_ids:
            # Grab events
            events += db(db.events.related_ticket == ptid).select().as_list()
        
        # Get events pertaining to any assigned tickets
        assigned_tickets_ids = Helper.get_assigned_ticket_ids_for_user(user_id)
        
        for atid in assigned_tickets_ids:
            # Grab events
            atevents = db(db.events.related_ticket == atid).select().as_list()
            for atevent in atevents:
                if atevent not in events:
                    events.append(atevent) # does this code confuse you? GOOD
        
        # Sort and limit
        # TODO: This won't work well as the number of events gets very large
        events.sort(key=lambda x: x["id"], reverse=True)
        events = events[:3]

        return events