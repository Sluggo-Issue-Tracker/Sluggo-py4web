# help.py - backend code for help page and related functions
# part of Sluggo, a free and open source issue tracker
# Copyright (c) 2020 Slugbotics - see git repository history for individual committers
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""
This file defines the actions related to help
"""
import base64
import pathlib
import uuid
import os.path
from os import path

from py4web import action, request, abort, redirect, URL, Field
from .. common import db, session, T, cache, auth, signed_url, settings
from .. helper import Helper
from .. EventLogger import EventLogger
from ..components import userValidator

@action('help')
@action.uses(userValidator, 'help.html', auth.user)
def help():
    return(
        dict(
            base_url = URL(''),
            user=auth.get_user(),
            username=Helper.get_user_title(),
        )
    )

@action('get_help_page/<pagename>', method=['GET'])
@action.uses()
def get_helppage(pagename: str):
    print("GOT HELPFILE REQUEST FOR PAGE " + pagename)
    VALID_PAGENAMES = {
        'usage': 'USAGE.md',
        'attribution': 'ATTRIBUTION.md'
    }
    if pagename not in VALID_PAGENAMES:
        abort(403, "Not a valid help page.")

    help_file_path = settings.APP_FOLDER + "/" + VALID_PAGENAMES[pagename]

    if not path.exists(help_file_path):
        abort(404, "Help file not found; this is an error")

    helpFileContents = str()
    # Otherwise read and serve the file
    with open(help_file_path, 'r') as file:
        helpFileContents = file.read()

    return helpFileContents
