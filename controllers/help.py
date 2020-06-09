"""
This file defines the actions related to help
"""
import base64
import pathlib
import uuid

from py4web import action, request, abort, redirect, URL, Field
from .. common import db, session, T, cache, auth, signed_url
from .. helper import Helper
from .. EventLogger import EventLogger

@action('help')
@action.uses('help.html')
def help():
    return(
        dict(
            
        )
    )