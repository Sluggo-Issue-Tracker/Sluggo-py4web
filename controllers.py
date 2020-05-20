"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url
from . models import get_user_email, get_user_title, get_user_name


@action('index')
@action.uses('index.html', signed_url, auth.user)
def index():
    return dict(
        get_tickets_url = URL('get_tickets', signer=signed_url),
        add_tickets_url = URL('add_tickets', signer=signed_url),
        delete_tickets_url = URL('delete_tickets', signer=signed_url),
        edit_ticket_url = URL('edit_ticket', signer=signed_url),
        user_email = get_user_email(),
        username = get_user_title(),
        user=auth.get_user()
    )

@action('get_tickets')
@action.uses(signed_url.verify(), auth.user)
def get_tickets():
    tickets = db(db.tickets).select(orderby=~db.tickets.created).as_list()

    for ticket in tickets:
        ticket["ticket_author"] = get_user_name(ticket)
    return dict(tickets=tickets)


@action('add_tickets', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def add_tickets():
    id = db.tickets.insert(
        ticket_title=request.json.get('ticket_title'),
        ticket_text=request.json.get('ticket_text'),
        ticket_status=request.json.get('ticket_status'),
        ticket_priority=request.json.get('ticket_priority')
    )
    return dict(id=id)

@action('edit_ticket', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def edit_ticket():
    print(request.json);
    row = db(db.tickets.id == request.json.get('id')).select().first()
    print(row)
    row.update_record(ticket_title = request.json.get('ticket_title'),
                      ticket_text = request.json.get('ticket_text'),
                      ticket_status = request.json.get('ticket_status'),
                      ticket_priority = request.json.get('ticket_priority'))
    return "ok"

@action('delete_tickets', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def delete_tickets():
    id = request.json.get('id')
    if id is not None:
        db(db.tickets.id == id).delete()
        return "ok"
