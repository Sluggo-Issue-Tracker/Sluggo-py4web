"""
This file defines the database models
"""
import datetime

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
    return auth.current_user.get('first_name') + " " + auth.current_user.get('last_name')

def get_time():
    return datetime.datetime.utcnow()

# Use these tables.

db.define_table('task',
                Field('user_email', default=get_user_email),
                Field('task_text', 'text'),
                Field('task_status'),
                Field('created', 'datetime', default=get_time),
                Field('activated', 'datetime'),
                Field('deactivated', 'datetime')
                )



db.commit()
