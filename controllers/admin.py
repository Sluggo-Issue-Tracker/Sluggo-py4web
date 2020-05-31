"""
This file defines the actions related to index and homepages
possibly should be in the controller as users idk tho
"""
import base64
import pathlib
import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from yatl.helpers import A
from pydal.validators import *
from ..common import db, session, T, cache, auth, signed_url
from ..models import Helper



def get_info(users):
    if type(users) is not list:
        return

    for user in users:
        person = db(db.auth_user.id == user.get('user')).select().first()
        user["full_name"] = "%s %s" % \
                            (person.get('first_name'), person.get('last_name')) if person else "Unknown"
        user['tags_list'] = ", ".join(Helper.get_user_tag_by_name(user))
        user['bio'] = user['bio'][:40]
        user['role'] = user['role'].capitalize()
        user['user_email'] = person.get('email')




@action('admin')
@action.uses('admin.html', signed_url, auth.user)
def admin():
    user = db(db.users.user == Helper.get_user()).select().first()
    if user != None and user['role'] != "admin":
        redirect(URL('index'))



    return dict(
        get_users_url=URL('admin/get_users', signer=signed_url),
        get_unapproved_users_url=URL('admin/get_unapproved_users', signer=signed_url),
        set_role_url=URL('set_role', signer=signed_url),
        user_email=Helper.get_user_email(),
        username=Helper.get_user_title(),
        user=auth.get_user()
    )



@action('admin/get_unapproved_users')
@action.uses(signed_url.verify(), auth.user)
def get_unapproved_users():
    users = db(db.users.role == "unapproved").select().as_list()

    get_info(users)
    return dict(users=users)

@action('admin/get_users')
@action.uses(signed_url.verify(), auth.user)
def get_admin_users():
    users = db(db.users.role).select().as_list()

    get_info(users)
    return dict(users=users)


@action('set_role', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def edit_user():
    row = db(db.users.id == request.json.get('id')).select().first()

    if row is None:
        return

    row.update_record(role=request.json.get('role').lower())
    return "ok"
