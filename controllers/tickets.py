"""
This file defines the actions related to index and homepages
possibly should be in the controller as users idk tho
"""
import base64
import pathlib
import uuid

from py4web import action, request, abort, redirect, URL, Field
from ..common import db, session, T, cache, auth, signed_url
from ..models import get_user_email, get_user_title, get_user_name, get_user, \
    get_time, get_tags_list, get_user_tag_by_name, get_ticket_tags_by_id, get_sub_tickets_by_parent_id, \
    get_comment_thread_by_ticket_id


# helper methods


# http request handlers
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
        ticket_details_url=URL('ticket_details'),
        user_email=get_user_email(),
        username=get_user_title(),
        user=auth.get_user()
    )


@action('ticket_details/<ticket_id>', method=['GET'])
@action.uses('ticket_details.html', signed_url, auth.user)
def ticket_details(ticket_id=None):
    # return all the links that the front end will use of requests
    return dict(
        get_ticket_by_id_url=URL('get_ticket_by_id', ticket_id, signer=signed_url),
        add_tickets_url=URL('add_tickets', signer=signed_url),
        add_sub_ticket_url=URL('add_sub_ticket', signer=signed_url),
        edit_ticket_url=URL('edit_ticket', signer=signed_url),
        tickets_details_url=URL('ticket_details'),
        delete_tickets_url=URL('delete_ticket', signer=signed_url),
        get_all_tags=URL('get_tags', signer=signed_url),
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
        ticket["tag_list"] = get_ticket_tags_by_id(ticket.get('id'))

    return dict(tickets=tickets, ticket_tags=ticket_tags)


@action('get_ticket_by_id/<ticket_id>')
@action.uses(signed_url.verify(), auth.user)
def get_ticket_by_id(ticket_id=None):

    ticket = db(db.tickets.id == ticket_id).select().as_list()[0]

    ticket["ticket_author"] = get_user_name(ticket)
    ticket["tag_list"] = get_ticket_tags_by_id(ticket.get('id'))
    ticket["sub_tickets"] = get_sub_tickets_by_parent_id(ticket.get('id'))

    return dict(ticket=ticket)


@action('get_comment_thread')
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
        tag_id = db.global_tag.insert(tag_name=tag.get('tag_name')) if global_tag is None else global_tag.id
        db.ticket_tag.insert(ticket_id=ticket_id, tag_id=tag_id)

    ticket = db(db.tickets.id == ticket_id).select().as_list()

    ticket[0]["tag_list"] = request.json.get('tag_list')

    return dict(ticket=ticket[0])  # return the record


@action('add_sub_ticket', method='POST')
@action.uses(signed_url.verify(), auth.user, db)
def add_sub_ticket():
    # repetition sucks but i don't want to make classes just yet
    parent_id = request.json.get('parent_id')
    child_id = db.tickets.insert(
        ticket_title=request.json.get('ticket_title'),
        ticket_text=request.json.get('ticket_text'),
    )

    for tag in request.json.get('tag_list'):
        global_tag = db(db.global_tag.tag_name == tag.get('tag_name')).select(db.global_tag.id).first()
        tag_id = db.global_tag.insert(tag_name=tag.get('tag_name')) if global_tag is None else global_tag.id
        db.ticket_tag.insert(ticket_id=child_id, tag_id=tag_id)

    ticket = db(db.tickets.id == child_id).select().as_list()

    ticket[0]["tag_list"] = request.json.get('tag_list')

    db.sub_tickets.insert(parent_id=parent_id, child_id=child_id)

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
