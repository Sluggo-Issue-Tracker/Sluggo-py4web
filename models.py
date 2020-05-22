"""
This file defines the database models
"""
from datetime import datetime, timezone

from . common import db, Field, auth
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user_title():
    return auth.current_user.get('first_name') + " " + auth.current_user.get('last_name') if auth.current_user else None

def get_user_name(entry):
    r = db(db.auth_user.email == entry.get("user_email")).select().first()
    return r.first_name + " " + r.last_name if r is not None else "Unknown"

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.now(timezone.utc)

def time_str():
    time = get_time()
    return time.strftime("%m/%d/%Y %H:%M:%S %Z")

# TODO: Do we want separate projects to be included in the db?

db.define_table(
    'users',
    Field('user', 'reference auth_user', default=get_user()),
    Field('role'),
    Field('bio'),
)

# db.define_table(
#     'ticket',
#     Field('title'),
#     Field('due_date'), # TODO find date format + serialize
#     Field('description')

#     # Additional properties that must be queried:
#     # Dependenencies -> select all children from ticket_rels
#     # Dependents -> select all parents from ticket_rels
#     # Percentage -> BFS and give proportion (should cache longterm)
# )


db.define_table(
    'tickets',
    Field('user_email', default=get_user_email),
    Field('ticket_title', 'text'),
    Field('ticket_text', 'text'),
    Field('created', 'datetime', default=get_time),
    Field('activated', 'datetime', default=get_time),
    Field('completed', 'datetime', default=get_time)
)


db.define_table( # credit tdimhcsleumas for design
    'sub_tickets',
    Field('parent', 'reference tickets'),
    Field('child', 'reference tickets')
)

db.define_table(
    'ticket_tag',
    Field('ticket_id', 'reference tickets'),
    Field('tag_name', 'text')
)

db.define_table(
    'user_tags',
    Field('user_id', 'reference users'),
    Field('tag_name'),
)

# TODO tags, roles, other fun things that require relationships

# TODO readables vs not readables (relevant? can we even use default forms?)
# TODO requirements for forms (again, is this even relevant?)

db.ticket_rels.ondelete = 'NO ACTION' # We don't want relationships to affect tickets
db.commit()
