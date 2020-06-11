"""
This file defines the actions related to index and homepages
possibly should be in the controller as users idk tho
"""
import base64
import pathlib
import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.core import HTTP
from datetime import datetime
from dateutil.parser import parse
from ..common import db, session, T, cache, auth, signed_url
from ..models import Helper
from ..components import userValidator, comments
from ..EventLogger import EventLogger

# if only i could mark something const in python : (
# idx 0 should always be not started
# idx 1 should always be in progress
# idx 2 should always be completed
# this is better than doing string comparisons since i'm really good at
# misspelling stuff
valid_statuses = ["Not Started", "In Progress", "Completed"]


# helper methods
def generate_ticket_status(ticket):
    action = -1
    if ticket is not None:
        if ticket.get('started') is not None:
            action = 2 if ticket.get('completed') is not None else 1
        else:
            action = 0
    return valid_statuses[action] if action != -1 else action


# Read -----------------------------------------------------------------------
@action('tickets')
@action.uses(userValidator, 'tickets.html', signed_url, auth.user)
def tickets():
    tag_id = request.query.get("tag_id")
    assignee_id = request.query.get("assignee_id")
    return dict(
        get_tickets_url=URL('get_tickets', signer=signed_url),
        add_tickets_url=URL('add_tickets', signer=signed_url),
        delete_tickets_url=URL('delete_tickets', signer=signed_url),
        edit_ticket_url=URL('edit_ticket', signer=signed_url),
        add_ticket_tag_url=URL('add_ticket_tag', signer=signed_url),
        get_tags_url=URL('get_tags', signer=signed_url),
        get_pinned_tickets_url=URL('get_pinned_tickets', signer=signed_url),
        get_users_url=URL('users/get_users', signer=signed_url),
        get_all_progress=URL('get_all_progress', signer=signed_url),
        pin_ticket_url=URL('pin_ticket', signer=signed_url),
        ticket_details_url=URL('ticket_details'),
        get_users_by_tag_list_url=URL('get_users_by_tag_list', signer=signed_url),
        user_email=Helper.get_user_email(),
        username=Helper.get_user_title(),
        user=auth.get_user(),
        tag_id=tag_id,
        assignee_id=assignee_id
    )


# another floater, perhaps this should be a class


@action('ticket_details/<ticket_id>', method=['GET'])
@action.uses(userValidator, 'ticket_details.html', signed_url, auth.user, comments)
def ticket_details(ticket_id=None):
    # return all the links that the front end will use of requests
    full_user = db(db.users.user == Helper.get_user()).select().first()
    user = auth.get_user()
    user["role"] = full_user.role if full_user else None

    if not full_user or full_user.role == "unapproved":
        redirect(URL('tickets'))

    if not ticket_id.isnumeric() or not db(db.tickets.id == ticket_id).select().first():
        redirect(URL('tickets'))

    return dict(
        get_ticket_by_id_url=URL('get_ticket_by_id', ticket_id),
        get_tickets_url=URL('get_possible_subtickets', ticket_id),
        get_pinned_tickets_url=URL('get_pinned_tickets', signer=signed_url),
        pin_ticket_url=URL('pin_ticket', signer=signed_url),
        add_tickets_url=URL('add_tickets', signer=signed_url),
        edit_ticket_url=URL('edit_ticket', signer=signed_url),
        tickets_details_url=URL('ticket_details'),
        ticket_page_url=URL('tickets'),
        delete_tickets_url=URL('delete_tickets', signer=signed_url),
        get_all_tags=URL('get_tags'),
        get_all_progress=URL('get_all_progress'),
        get_users_url=URL('users/get_users', signer=signed_url),
        delete_tag_url=URL('delete_tag', signer=signed_url),
        update_progress_url=URL('update_ticket_progress', signer=signed_url),
        assign_user_url=URL('assign_user', signer=signed_url),
        user_email=Helper.get_user_email(),
        username=Helper.get_user_title(),
        user=user,
        comments=comments(id=ticket_id),
        add_subticket_url=URL('add_subticket', signer=signed_url),
        get_ticket_completion_url=URL('get_ticket_completion', ticket_id),
    )


@action('get_tags')
@action.uses(auth.user)
def get_tags():
    tags = db(db.global_tag.approved == True).select(orderby=db.global_tag.tag_name).as_list()
    return dict(tags=tags)


@action('get_all_progress')
@action.uses(auth.user)
def get_all_progress():
    return dict(valid_statuses=valid_statuses)


@action('get_tickets')
@action.uses(auth.user)
def get_tickets():
    tickets = db(db.tickets).select(orderby=~db.tickets.created).as_list()
    ticket_tags = db(db.global_tag.approved == True).select().as_list()

    for ticket in tickets:
        ticket["ticket_author"] = Helper.get_user_name(ticket)
        ticket["tag_list"] = Helper.get_ticket_tags_by_id(ticket.get('id'))
        ticket["status"] = generate_ticket_status(ticket)

    return dict(tickets=tickets, ticket_tags=ticket_tags)


@action('get_ticket_by_id/<ticket_id>')
@action.uses(auth.user)
def get_ticket_by_id(ticket_id=None):
    ticket = db(db.tickets.id == ticket_id).select().as_list()[0]
    current = db(db.users.user == auth.current_user.get('id')).select(db.users.role).first()

    ticket["ticket_author"] = Helper.get_user_name(ticket)
    ticket["tag_list"] = Helper.get_ticket_tags_by_id(ticket.get('id'))
    print(ticket['tag_list'])
    ticket["status"] = generate_ticket_status(ticket)
    ticket["sub_tickets"] = Helper.get_sub_tickets_by_parent_id(ticket.get('id'))

    assigned_user = db(db.auth_user.id == ticket.get('assigned_user')).select(
        db.users.ALL, db.auth_user.first_name, db.auth_user.last_name, db.auth_user.email,
        left=(db.auth_user.on(db.auth_user.id == db.users.user))).as_list()

    assigned_user = list(map(lambda x: {**x["users"], **x["auth_user"]}, assigned_user))

    for user in assigned_user:
        user["full_name"] = "%s %s" % \
                            (user.get('first_name'), user.get('last_name')) if user else "Unknown"
        user['user_email'] = user.get('email')

    if len(assigned_user) > 0:
        assigned_user = assigned_user[0]
    else:
        assigned_user = None

    editable = auth.current_user.get('email') == ticket.get('user_email') or current.get('role') == 'admin'

    return dict(ticket=ticket, assigned_user=assigned_user, editable=editable)


# MARK: Ticket Pinning
@action('get_pinned_tickets', method="GET")
@action.uses(auth.user, db)
def get_pinned_tickets():  # grabs pinned tickets for logged in user
    # Grab the current user's ID
    userID = Helper.get_user()
    if userID is None:
        abort(500, "No User ID obtained (is this possible?")

    # Query for pinned tickets given user ID
    pinnedTicketsQuery = db(db.user_pins.auth_user_id == userID).select().as_list()
    pinnedTickets = list(map(lambda x: x['ticket_id'], pinnedTicketsQuery))
    return (
        dict(
            pinned_tickets=pinnedTickets
        )
    )


# recursively count the number of complete subtickets before counting the root ticket
def _get_ticket_completion(ticket_id):
    completed = discovered = 0
    sub_tickets = db(db.sub_tickets.parent_id == ticket_id).select()

    for sub_ticket in sub_tickets:
        sub_completed, sub_discovered = _get_ticket_completion(sub_ticket.child_id)
        completed += sub_completed
        discovered += sub_discovered

    ticket = db(db.tickets.id == ticket_id).select(db.tickets.completed).first()
    if ticket.completed is not None:
        completed += 1
    discovered += 1

    return completed, discovered


@action('get_ticket_completion/<ticket_id>', method="GET")
@action.uses(auth.user, db)
def get_ticket_completion(ticket_id=None):
    if not ticket_id:
        raise HTTP(500)

    completed, discovered = _get_ticket_completion(ticket_id)

    return dict(percentage=completed / discovered if discovered != 0 else 0)


def _get_ancestor_list(ticket_id, ancestors):
    parents = db(db.sub_tickets.child_id == ticket_id).select(db.sub_tickets.parent_id).as_list()
    for parent in parents:
        _get_ancestor_list(parent.get('parent_id'), ancestors)
        ancestors.append(parent.get('parent_id'))


def _get_descendants_list(ticket_id, descendants):
    children = db(db.sub_tickets.parent_id == ticket_id).select(db.sub_tickets.child_id).as_list()
    for child in children:
        _get_ancestor_list(child.get('child_id'), descendants)
        descendants.append(child.get('child_id'))


@action('get_possible_subtickets/<ticket_id>', method="GET")
@action.uses(auth.user, db)
def get_possible_subtickets(ticket_id=None):
    if not ticket_id:
        raise HTTP(500)

    tickets = db(db.tickets).select().as_list()
    ancestors = []
    _get_ancestor_list(ticket_id, ancestors)
    descendants = []
    _get_descendants_list(ticket_id, descendants)
    invalid_list = ancestors + descendants + [int(ticket_id)]
    print(invalid_list)

    valid_tickets = []
    for ticket in tickets:
        if ticket.get("id") not in invalid_list:
            valid_tickets.append(ticket)

    return dict(tickets=valid_tickets)


# create ----------------------------------------------------------------------------------------------------

# helper for adding tags
def register_tag(tag_list, ticket_id):
    for tag in tag_list:
        global_tag = db(db.global_tag.id == tag.get('id')).select(db.global_tag.id).first()
        tag_id = db.global_tag.insert(tag_name=tag.get('tag_name')) if global_tag is None else global_tag.id
        db.ticket_tag.insert(ticket_id=ticket_id, tag_id=tag_id)


@action('add_tickets', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def add_tickets():
    parent_id = request.json.get('parent_id')
    ticket_title = request.json.get('ticket_title')
    ticket_text = request.json.get('ticket_text')
    ticket_due_date = request.json.get('due_date')
    assigned_user = request.json.get('assigned_user')

    print("the due date is " + ticket_due_date)

    ticket_id = db.tickets.insert(
        ticket_title=ticket_title,
        ticket_text=ticket_text,
        due=parse(ticket_due_date) if ticket_due_date else None,
        assigned_user=assigned_user.get('user') if type(assigned_user) is dict else None
    )

    # apply tags
    register_tag(request.json.get('tag_list'), ticket_id)
    ticket = db(db.tickets.id == ticket_id).select().as_list()
    ticket[0]["tag_list"] = request.json.get('tag_list')

    # create subticket entry if parent_id set
    if parent_id is not None:
        db.sub_tickets.insert(parent_id=parent_id, child_id=ticket_id)

    return dict(ticket=ticket[0])  # return the record


@action('add_subticket', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def add_subticket():
    parent_id = request.json.get('parent_id')
    child_id = request.json.get('child_id')

    if not parent_id or not child_id:
        raise HTTP(500)

    db.sub_tickets.update_or_insert(parent_id=parent_id, child_id=child_id)
    ticket = db(db.tickets.id == child_id).select().as_list()[0]

    return dict(ticket=ticket)


@action('pin_ticket', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def pin_ticket():
    ticketID = request.json.get("ticket_id")
    if ticketID is None:
        abort(400, "Ticket ID to pin not provided")
    userID = Helper.get_user()
    if userID is None:
        abort(500, "No User ID obtained (is this possible?)")

    potentialPinQuery = db((db.user_pins.auth_user_id == userID) & \
                           (db.user_pins.ticket_id == ticketID))  # the query
    pin = potentialPinQuery.select()  # fetch query from db
    if not pin:
        # Create a pin record
        db.user_pins.insert(auth_user_id=userID, ticket_id=ticketID)
    else:
        # Delete it
        potentialPinQuery.delete()
    return "ok"


# update --------------------------------------------------------------------------------------------------
@action('edit_ticket', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def edit_ticket():
    ticket_id = request.json.get('id')
    title = request.json.get('title')
    text = request.json.get('text')
    tag_list = request.json.get('tag_list')
    due_date = request.json.get('due_date')  # TODO: implement due dates here

    ticket = db.tickets[ticket_id]
    if ticket is None:
        abort(400, "could not find specified ticket")

    if type(tag_list) is not list and tag_list is not None:
        print("wrong type for tag_list")
        abort(500, "wrong type for tag_list")

    if type(title) is not str:
        print("wrong values for title or text")
        abort(500, "wrong values for title and text")

    ticket.update_record(ticket_title=title.strip(),
                         ticket_text=text.strip() if text else "",
                         due=parse(due_date) if due_date else None)

    current_tickets = Helper.get_ticket_tags_by_id(ticket_id)

    # tag ids should be unique so this should not cause an error
    tag_set = set()
    for tag in tag_list:
        tag_id = tag.get('id')
        if tag_id is None:
            tag_id = db(db.global_tag).insert(tag_name=tag.get('tag_name'))
        tag_set.add(tag_id)

    current_set = {tag.get('id') for tag in current_tickets} if current_tickets is not None else set()

    # yay inefficient tag update, set difference does not work on sets full of dicts
    for tag_id in current_set.difference(tag_set):
        db((db.ticket_tag.ticket_id == ticket_id) & (db.ticket_tag.tag_id == tag_id)).delete()

    for tag_id in tag_set.difference(current_set):
        db.ticket_tag.insert(ticket_id=ticket_id, tag_id=tag_id)

    return "ok"


@action('update_ticket_progress', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def update_ticket_progress():
    action = request.json.get('status')
    ticket_id = request.json.get('ticket_id')

    ticket = db.tickets[ticket_id]
    if ticket is None:
        abort(400, "no such ticket exists")

    idx = valid_statuses.index(action)
    print(idx)
    if idx == 0:  # not started
        EventLogger.log_status_change("Not Started", ticket_id, Helper.get_user())
        ticket.update_record(started=None, completed=None)

    elif idx == 1:  # in progress
        EventLogger.log_status_change("In Progress", ticket_id, Helper.get_user())
        ticket.update_record(started=Helper.get_time(), completed=None)

    elif idx == 2:  # completed
        EventLogger.log_status_change("Completed", ticket_id, Helper.get_user())
        ticket.update_record(
            started=Helper.get_time() if ticket.started is None else ticket.started,
            completed=Helper.get_time()
        )

    return dict(ticket_id=ticket_id, status=action)


@action('assign_user', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def assign_user():
    ticket_id = request.json.get('ticket_id')
    user_id = request.json.get('user_id')

    print(user_id)

    if ticket_id is None:
        return dict(message="ids are undefined")

    ticket = db.tickets[ticket_id]
    ticket.update_record(assigned_user=user_id)
    return dict(message="success")


# delete ---------------------------------------------------------------------------------
@action('delete_tickets', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def delete_tickets():
    id = request.json.get('id')
    if id is not None:
        db(db.tickets.id == id).delete()
        return "ok"


@action('delete_tag', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def delete_tag():
    tag_id = request.json.get("tag_id")
    ticket_id = request.json.get("ticket_id")
    handle = db((db.ticket_tag.tag_id == tag_id) & (db.ticket_tag.ticket_id == ticket_id)).delete()
    return dict(handle=handle)
