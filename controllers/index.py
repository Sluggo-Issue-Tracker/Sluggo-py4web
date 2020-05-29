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

@action('clean')
@action.uses(auth.user, db)
def clean():
    db(db.users).delete()
    db(db.tickets).delete()
    db(db.global_tag).delete()
    return "ok"

def get_tag_string_for_list(x):
    print(x)
    final = ""
    if len(x) == 0:
        return "No Tags "
    for t in x:
        final = final + "#" + t + " "
    return final

# MARK: Index
@action('index')
@action.uses('index.html', signed_url, auth.user, db)
def tickets():
    user = db(db.users.user == Helper.get_user()).select().first()
    if user == None:
        redirect(URL('create_profile'))
        # TODO: is this ^ a comprehensive enough redirect?

    # Grab pinned tickets
    # Grab the current user's ID
    userID = Helper.get_user()
    if userID is None:
        abort(500, "No User ID obtained (is this possible?")

    # Query for pinned tickets given user ID
    pinnedTicketsIDQuery = db(db.user_pins.auth_user_id == userID).select().as_list()
    pinnedTicketsIDs = list(map(lambda x: x['ticket_id'], pinnedTicketsIDQuery))

    # Now grab the tickets
    pinned_tickets = []
    for ptid in pinnedTicketsIDs:
        # Query for the ticket
        foundTicket = db(db.tickets.id == ptid).select().first()
        print(foundTicket)
        if foundTicket is None:
            pass # TODO: This should not happen but fixes an oversight of mine deleting
                # TODO: Are we deleting ticket rels?
        foundTicket.tags = get_tag_string_for_list(list(map(lambda x: x['tag_name'], Helper.get_ticket_tags_by_id(foundTicket.get('id')))))
        # check if completed and set styling
        if foundTicket.completed is not None:
            foundTicket.style = "is-success"
        else:
            foundTicket.style = "is-info"
        pinned_tickets.append(foundTicket)

    # MARK: Grab tags
    tags = db(db.user_tag.user_id == user.get('id')).select(db.global_tag.tag_name, left=db.global_tag.on(
            db.global_tag.id == db.user_tag.tag_id))
    print("THIS")
    print(tags)
    user_tags = []
    for tag in tags:
        tag['tag_display_title'] = tag.get('tag_name').capitalize()
        tag['tag_redirect_url'] = URL('tickets', vars=dict(tag=tag.tag_name))
        user_tags.append(tag)

    return(dict(
        user_email=Helper.get_user_email(),
        username=Helper.get_user_title(),
        user=auth.get_user(),
        date=str(Helper.get_time().isoformat()),
        pinned_tickets = pinned_tickets,
        user_tags = user_tags
    ))

