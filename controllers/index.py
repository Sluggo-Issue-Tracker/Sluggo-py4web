"""
This file defines the actions related to index and homepages
possibly should be in the controller as users idk tho
"""
import base64
import pathlib
import uuid

from py4web import action, request, abort, redirect, URL, Field
from .. common import db, session, T, cache, auth, signed_url
from .. helper import Helper
from .. EventLogger import EventLogger

@action('clean')
@action.uses(auth.user, db)
def clean():
    db(db.users).delete()
    db(db.tickets).delete()
    db(db.global_tag).delete()
    db(db.sub_tickets).delete()
    db(db.ticket_tag).delete()
    db(db.user_tag).delete()
    db(db.user_pins).delete()
    db(db.comment).delete()
    return "ok"


# MARK: Index
@action('index')
@action.uses('index.html', signed_url, auth.user)
def index():
    user = db(db.users.user == Helper.get_user()).select().first()
    if user == None:
        redirect(URL('create_profile'))
        # TODO: is this ^ a comprehensive enough redirect?

    # Grab pinned tickets
    pinned_tickets = Helper.get_tickets_for_ids(Helper.get_pinned_ticket_ids_for_user(Helper.get_user()))

    # Attach tag list to tickets
    Helper.attach_tags_for_tickets(pinned_tickets)

    # Grab user tags
    user_tags = Helper.get_web_tag_list_for_user_id(Helper.get_user())

    # Grab priority tickets
    user_id = Helper.get_our_user_id(Helper.get_user())
    priority_tickets = Helper.get_priority_ticket_ids_for_user(user_id)

    # Attach data to priority tickets
    Helper.attach_tags_for_tickets(priority_tickets)
    Helper.attach_web_due_for_tickets(priority_tickets)
    # Grab recent updates
    recentUpdates = EventLogger.get_recent_updates_for_user(Helper.get_user())
    Helper.attach_web_names_for_events(recentUpdates)
    print(Helper.safe_json_dumps(recentUpdates))

    return(dict(
        user_email=Helper.get_user_email(),
        username=Helper.get_user_title(),
        user=auth.get_user(),
        user_id = Helper.get_user(),
        date=str(Helper.get_time().isoformat()),
        ticket_details_url = URL('ticket_details'),
        tickets_url = URL('tickets'),
        get_icons_url = URL('users', 'get_icons'),
        pinned_tickets = Helper.safe_json_dumps(pinned_tickets),
        priority_tickets = Helper.safe_json_dumps(priority_tickets),
        assigned_tickets_count = Helper.fetch_assigned_count_for_user(Helper.get_user()),
        user_tags = Helper.safe_json_dumps(user_tags),
        recent_events = Helper.safe_json_dumps(recentUpdates),
        admin=Helper.get_role() == 'Admin'
    ))

