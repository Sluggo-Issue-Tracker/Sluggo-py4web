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


from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url
from . models import get_user_email, get_user_title, get_user_name, get_user

# --------------------------------------------------- TICKETS --------------------------------------------------- #
@action('index')
@action.uses('index.html', signed_url, auth.user)
def index():
    user = db(db.users.auth == get_user()).select().first()
    if user == None:
        redirect(URL('create_profile'))

    return dict(
        get_tickets_url = URL('get_tickets', signer=signed_url),
        add_tickets_url = URL('add_tickets', signer=signed_url),
        delete_tickets_url = URL('delete_tickets', signer=signed_url),
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



@action('delete_tickets', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def delete_tickets():
    id = request.json.get('id')
    if id is not None:
        db(db.tickets.id == id).delete()
        return "ok"


# --------------------------------------------------- USERS --------------------------------------------------- #

USERS = [ {"first_name": "Andrew", "last_name": "Gavgavian", "user_email" : "agavgavi@ucsc.edu", "role": "Administrator", "bio":"Hi mom!"},
          {"first_name": "Isaac", "last_name": "Trimble-Pederson", "user_email" : "itrimble@ucsc.edu", "role": "Administrator", "bio":"Test Bio"},
          {"first_name": "Samuel", "last_name": "Schmidt", "user_email" : "sadschmi@ucsc.edu", "role": "Systems", "bio":"Shit"}]

@action('users/setup')
@action.uses( auth.user, db)
def setup():
    db(db.users).delete()
    for u in USERS:
        db.users.insert(first_name=u.get('first_name'),
                        last_name=u.get('last_name'),
                        user_email=u.get('user_email'),
                        role=u.get('role'),
                        bio=u.get('bio'))
    return "ok"

@action('users')
@action.uses('users.html', signed_url, auth.user)
def users():
    return dict(
        get_users_url = URL('users/get_users', signer=signed_url),
        get_icons_url = URL('users/get_icons', signer=signed_url),
        user_email = get_user_email(),
        username = get_user_title(),
        user=auth.get_user()
    )


@action('create_profile', method=['GET', 'POST'])
@action.uses('create_profile.html', db, session, auth.user)
def create_user():
    user = db(db.users.auth == get_user()).select().first()
    if user != None:
        redirect(URL('index'))

    form = Form(db.users,
                csrf_session=session,
                formstyle=FormStyleBulma)



    if form.accepted:
        redirect(URL('index'))

    return dict(form=form, user=auth.get_user(), username = get_user_title())






@action('users/get_users')
@action.uses(signed_url.verify(), auth.user)
def get_users():
    users = db(db.users).select().as_list()

    for user in users:
        user["icon"] = "%s-%s.jpg" % (user.get('first_name').lower(), user.get('last_name').lower())
        user["full_name"] = "%s %s" % (user.get('first_name'), user.get('last_name'))
    return dict(users=users)


@action('users/get_icons')
@action.uses(signed_url.verify())
def get_img():
    """Returns a single image, URL encoded."""
    # Reads the image.
    img_name = request.params.img
    img_file = pathlib.Path(__file__).resolve().parent / 'static' / 'images' / img_name
    with img_file.open(mode='rb') as f:
        img_bytes = f.read()
        b64_image = base64.b64encode(img_bytes).decode('utf-8')
    # Returns the image bytes, base64 encoded, and with the correct prefix.
    return dict(imgbytes="data:image/jpeg;base64," + b64_image)
