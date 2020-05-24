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
import base64
import pathlib
import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from yatl.helpers import A
from pydal.validators import *
from . common import db, session, T, cache, auth, signed_url
from . models import get_user_email, get_user_title, get_user_name, get_user, get_time, get_tags_list, get_user_tag_by_name



@action('clean')
@action.uses(auth.user, db)
def clean():
    db(db.users).delete()
    db(db.tickets).delete()
    db(db.global_tag).delete()
    return "ok"


# MARK: Index
@action('index')
@action.uses('index.html', signed_url, auth.user)
def tickets():
    user = db(db.users.user == get_user()).select().first()
    if user == None:
        redirect(URL('create_profile'))
        # TODO: is this ^ a comprehensive enough redirect?

    return(dict(
        user_email=get_user_email(),
        username=get_user_title(),
        user=auth.get_user(),
        date=str(get_time().isoformat())
    ))

# --------------------------------------------------- TICKETS --------------------------------------------------- #
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


# --------------------------------------------------- USERS --------------------------------------------------- #

@action('users')
@action.uses('users.html', signed_url, auth.user)
def users():
    return dict(

        get_users_url = URL('users/get_users', signer=signed_url),
        get_icons_url = URL('users/get_icons', signer=signed_url),
        edit_user_url = URL('edit_user', signer=signed_url),
        user_email = get_user_email(),
        username = get_user_title(),
        user=auth.get_user()
    )


@action('create_profile', method=['GET'])
@action.uses('create_profile.html', db, session, auth.user, signed_url)
def create_user():
    user = db(db.users.user == get_user()).select().first()
    if user != None:
        redirect(URL('index'))

    return dict(
        add_user_url=URL('add_user', signer=signed_url),
        user=auth.get_user(),
        username = get_user_title(),
        admin=db(db.users).isempty(),
        tags=get_tags_list()
    )


@action('add_user', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def add_user():
    u_id = db.users.insert(
        role="admin" if db(db.users).isempty() else "member",
        bio=request.json.get('bio'),
        user=get_user(),
    )

    tags = request.json.get('tags')

    for tag in tags:
        # get the tag if it is stored in database
        t_id = db(db.global_tag.tag_name == tag.lower()).select().first()

        if(t_id == None):
            # if tag isn't stored in database, create new tags
            t_id = db.global_tag.insert(tag_name=tag.lower())

        # now we insert tags in this many to many relationship
        db.user_tag.insert(
            user_id=u_id,
            tag_id=t_id
        )
    return "ok"


@action('users/get_users')
@action.uses(signed_url.verify(), auth.user)
def get_users():
    users = db(db.users).select().as_list()


    for user in users:
        person = db(db.auth_user.id == user.get('user')).select().first()
        user["icon"] = "%s-%s.jpg" % \
                       (person.get('first_name').lower(), person.get('last_name').lower()) if person else "Unknown"
        user["full_name"] = "%s %s" % \
            (person.get('first_name'), person.get('last_name')) if person else "Unknown"
        user['tags_list'] = get_user_tag_by_name(user)
        user['user_email'] = person.get('email')


    return dict(users=users,tags=get_tags_list())


@action('edit_user', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def edit_user():
    row = db(db.users.id == request.json.get('id')).select().first()
    user = db(db.auth_user.id == row.get('user')).select().first()

    row.update_record(bio=request.json.get('bio'),
                      role=request.json.get('role'))

    names = request.json.get('full_name').split()


    tags = request.json.get('tags_list')
    old_tags = get_user_tag_by_name(row)

    missing = set(old_tags).difference(tags)
    added = set(tags).difference(old_tags)

    # these tags are to be deleted from the user
    for tag in missing:
        # get the tag if it is stored in database
        t_id = db(db.global_tag.tag_name == tag.lower()).select().first()

        if(t_id == None):
            # if tag isn't stored in database, create new tags
            t_id = db.global_tag.insert(tag_name=tag.lower())

        db((db.user_tag.user_id == request.json.get('id')) & (db.user_tag.tag_id == t_id)).delete()

    # these tags are to be added to the user
    for tag in added:
        # get the tag if it is stored in database
        t_id = db(db.global_tag.tag_name == tag.lower()).select().first()

        if(t_id == None):
            # if tag isn't stored in database, create new tags
            t_id = db.global_tag.insert(tag_name=tag.lower())


        # now we insert tags in this many to many relationship
        db.user_tag.update_or_insert((db.user_tag.user_id == request.json.get('id')) & (db.user_tag.tag_id == t_id),
            user_id=request.json.get('id'),
            tag_id=t_id
        )

    user.update_record(first_name=names[0], last_name=names[1])
    return "ok"


@action('users/get_icons')
@action.uses(signed_url.verify())
def get_img():
    """Returns a single image, URL encoded."""
    # Reads the image.
    img_name = request.params.img
    img_file = pathlib.Path(__file__).resolve().parent / 'static' / 'images' / img_name
    if not img_file.exists():
        img_file = pathlib.Path(__file__).resolve().parent / 'static' / 'images' / "default.jpg"
    with img_file.open(mode='rb') as f:
        img_bytes = f.read()
        b64_image = base64.b64encode(img_bytes).decode('utf-8')
    # Returns the image bytes, base64 encoded, and with the correct prefix.
    return dict(imgbytes="data:image/jpeg;base64," + b64_image)
