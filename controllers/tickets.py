"""
This file defines the actions related to index and homepages
possibly should be in the controller as users idk tho
"""
import base64
import pathlib
import uuid

from py4web import action, request, abort, redirect, URL, Field
from .. common import db, session, T, cache, auth, signed_url
from .. models import get_user_email, get_user_title, get_user_name, get_user, get_time, get_tags_list, get_user_tag_by_name


@action('tickets')
@action.uses('tickets.html', signed_url, auth.user)
def tickets():
    return dict(
        get_tickets_url=URL('get_tickets', signer=signed_url),
        add_tickets_url=URL('add_tickets', signer=signed_url),
        delete_tickets_url=URL('delete_tickets', signer=signed_url),
        edit_ticket_url=URL('edit_ticket', signer=signed_url),
        add_ticket_tag_url=URL('add_ticket_tag', signer=signed_url),
        get_tags_url=URL('get_tags', signer=signed_url),
        get_pinned_tickets_url = URL('get_pinned_tickets', signer=signed_url),
        pin_ticket_url = URL('pin_ticket', signer=signed_url),
        user_email=get_user_email(),
        username=get_user_title(),
        user=auth.get_user()
    )


# tag stuff
@action('get_tags')
@action.uses(signed_url.verify(), auth.user)
def get_tags():
    tags = db(db.global_tag).select(orderby=db.global_tag.tag_name).as_list()
    return dict(tags=tags)


@action('get_tickets')
@action.uses(signed_url.verify(), auth.user)
def get_tickets():
    tickets = db(db.tickets).select(orderby=~db.tickets.created).as_list()
    ticket_tags = db(db.global_tag).select().as_list()

    for ticket in tickets:
        ticket["ticket_author"] = get_user_name(ticket)

        ticket["tag_list"] = db(db.ticket_tag.ticket_id == ticket.get("id")).select \
            (db.global_tag.tag_name,
             left=db.global_tag.on(
                 db.global_tag.id == db.ticket_tag.tag_id)).as_list()

    return dict(tickets=tickets, ticket_tags=ticket_tags)


@action('add_tickets', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def add_tickets():
    ticket_id = db.tickets.insert(
        ticket_title=request.json.get('ticket_title'),
        ticket_text=request.json.get('ticket_text'),
    )

    print(request.json.get('tag_list'))

    for tag in request.json.get('tag_list'):
        global_tag = db(db.global_tag.tag_name == tag.get('tag_name')).select(db.global_tag.id).first()
        db.ticket_tag.insert(ticket_id=ticket_id, tag_id=global_tag.id)

    ticket = db(db.tickets.id == ticket_id).select().as_list()

    ticket[0]["tag_list"] = request.json.get('tag_list')

    return dict(ticket=ticket[0])  # return the record


@action('add_ticket_tag', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def add_ticket_tag():
    ticket_id = request.json.get('ticket_id')
    for tag in request.json.get('tags'):
        tag_name = tag.name
        if tag_name is not None and ticket_id is not None:
            tag = db(db.global_tag.tag_name == tag_name).select().first()
            tag_id = db.global_tag.insert(tag_name=tag_name) if tag is None else tag.id
            db.ticket_tag.insert(tag_id=tag_id, ticket_id=ticket_id)

    return 'ok'


@action('edit_ticket', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def edit_ticket():
    print(request.json)
    row = db(db.tickets.id == request.json.get('id')).select().first()
    print(row)
    row.update_record(ticket_title=request.json.get('ticket_title'),
                      ticket_text=request.json.get('ticket_text'),
                      ticket_status=request.json.get('ticket_status'),
                      ticket_priority=request.json.get('ticket_priority'))
    return "ok"


@action('delete_tickets', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def delete_tickets():
    id = request.json.get('id')
    if id is not None:
        db(db.tickets.id == id).delete()
        return "ok"

# MARK: Ticket Pinning
@action('get_pinned_tickets', method="GET")
@action.uses(signed_url.verify(), auth.user, db)
def get_pinned_tickets(): # grabs pinned tickets for logged in user
    # Grab the current user's ID
    userID = get_user()
    if userID == None:
        abort(500, "No User ID obtained (is this possible?")
    
    # Query for pinned tickets given user ID
    pinnedTicketsQuery = db(db.user_pins.auth_user_id == userID).select().as_list()
    pinnedTickets = list(map(lambda x: x['ticket_id'], pinnedTicketsQuery))
    return(
        dict(
            pinned_tickets = pinnedTickets
        )
    )

@action('pin_ticket', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def pin_ticket():
    ticketID = request.json.get("ticket_id")
    if ticketID is None:
        abort(400, "Ticket ID to pin not provided")
    userID = get_user()
    if userID is None:
        abort(500, "No User ID obtained (is this possible?)")
    
    potentialPinQuery = db((db.user_pins.auth_user_id == userID) & \
        (db.user_pins.ticket_id == ticketID)) # the query
    pin = potentialPinQuery.select() # fetch query from db
    if not pin:
        # Create a pin record
        db.user_pins.insert(auth_user_id=userID, ticket_id=ticketID)
    else:
        # Delete it
        potentialPinQuery.delete()
    return "ok"
    