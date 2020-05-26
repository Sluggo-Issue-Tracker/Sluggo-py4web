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


@action('users')
@action.uses('users.html', signed_url, auth.user)
def users():
    return dict(

        get_users_url=URL('users/get_users', signer=signed_url),
        get_icons_url=URL('users/get_icons', signer=signed_url),
        edit_user_url=URL('edit_user', signer=signed_url),
        user_email=Helper.get_user_email(),
        username=Helper.get_user_title(),
        user=auth.get_user()
    )


@action('create_profile', method=['GET'])
@action.uses('create_profile.html', db, session, auth.user, signed_url)
def create_user():
    user = db(db.users.user == Helper.get_user()).select().first()
    if user != None:
        redirect(URL('index'))

    return dict(
        add_user_url=URL('add_user', signer=signed_url),
        user=auth.get_user(),
        username=Helper.get_user_title(),
        admin=db(db.users).isempty(),
        tags=Helper.get_tags_list()
    )


@action('add_user', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def add_user():
    u_id = db.users.insert(
        role="admin" if db(db.users).isempty() else "member",
        bio=request.json.get('bio'),
        user=Helper.get_user(),
    )

    tags = request.json.get('tags')

    for tag in tags:
        # get the tag if it is stored in database
        t_id = db(db.global_tag.tag_name == tag.lower()).select().first()

        if (t_id == None):
            # if tag isn't stored in database, create new tags
            t_id = db.global_tag.insert(tag_name=tag.lower())

        # now we insert tags in this many to many relationship
        db.user_tag.insert(
            user_id=u_id,
            tag_id=t_id
        )
    return "ok"


def attach_user_information(users):
    if type(users) is not list:
        return

    print(users)

    for user in users:
        person = db(db.auth_user.id == user.get('user')).select().first()

        if person is None:
            break

        user["icon"] = "%s-%s.jpg" % \
                       (person.get('first_name').lower(), person.get('last_name').lower()) if person else "Unknown"
        user["full_name"] = "%s %s" % \
                            (person.get('first_name'), person.get('last_name')) if person else "Unknown"
        user['tags_list'] = Helper.get_user_tag_by_name(user)
        user['user_email'] = person.get('email')


@action('users/get_users')
@action.uses(signed_url.verify(), auth.user)
def get_users():
    users = db(db.users).select().as_list()

    attach_user_information(users)
    return dict(users=users, tags=Helper.get_tags_list())


@action('get_users_by_tag_list', method="POST")
@action.uses(signed_url.verify(), auth.user)
def get_users_by_tag_list():
    tag_list = request.json.get('tag_list')
    user_dict = dict()

    if type(tag_list) is not list:
        return dict(users=list())

    # all tags here should be defined in our list
    for tag in tag_list:
        tag_users = Helper.get_users_by_tag_id(tag.get('id'))
        attach_user_information(tag_users)

        # keyed in from id keeps these unique
        for user in tag_users:
            if user_dict.get(user["id"]) is None:
                user_dict[user["id"]] = user

    return dict(users=user_dict.values())


@action('edit_user', method="POST")
@action.uses(signed_url.verify(), auth.user, db)
def edit_user():
    row = db(db.users.id == request.json.get('id')).select().first()
    user = db(db.auth_user.id == row.get('user')).select().first()

    row.update_record(bio=request.json.get('bio'),
                      role=request.json.get('role'))

    names = request.json.get('full_name').split()

    tags = request.json.get('tags_list')
    old_tags = Helper.get_user_tag_by_name(row)

    missing = set(old_tags).difference(tags)
    added = set(tags).difference(old_tags)

    # these tags are to be deleted from the user
    for tag in missing:
        # get the tag if it is stored in database
        t_id = db(db.global_tag.tag_name == tag.lower()).select().first()

        if (t_id == None):
            # if tag isn't stored in database, create new tags
            t_id = db.global_tag.insert(tag_name=tag.lower())

        db((db.user_tag.user_id == request.json.get('id')) & (db.user_tag.tag_id == t_id)).delete()

    # these tags are to be added to the user
    for tag in added:
        # get the tag if it is stored in database
        t_id = db(db.global_tag.tag_name == tag.lower()).select().first()

        if (t_id == None):
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
    img_file = pathlib.Path(__file__).resolve().parent.parent / 'static' / 'images' / img_name
    if not img_file.exists():
        img_file = pathlib.Path(__file__).resolve().parent.parent / 'static' / 'images' / "default.jpg"
    with img_file.open(mode='rb') as f:
        img_bytes = f.read()
        b64_image = base64.b64encode(img_bytes).decode('utf-8')
    # Returns the image bytes, base64 encoded, and with the correct prefix.
    return dict(imgbytes="data:image/jpeg;base64," + b64_image)