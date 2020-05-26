"""
This file defines the actions related to index and homepages
possibly should be in the controller as users idk tho
"""
import base64
import pathlib
import uuid

from py4web import action, request, abort, redirect, URL, Field
from .. common import db, session, T, cache, auth, signed_url


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
        date=str(get_time().isoformat()),
        get_pinned_tickets_url = URL('get_pinned_tickets', signer=signed_url)
    ))

