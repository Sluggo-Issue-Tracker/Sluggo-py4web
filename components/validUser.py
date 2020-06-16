# validUser.py - user checking fixture for backend controllers
# part of Sluggo, a free and open source issue tracker
# Copyright (c) 2020 Slugbotics - see git repository history for individual committers
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""this fixture checks if a user is valid"""

from py4web import action, URL, request, redirect
from yatl.helpers import XML
from py4web.utils.url_signer import URLSigner
from py4web.core import Fixture, HTTP
from ..helper import Helper


class UserValidator(Fixture):

    def __init__(self, db):
        self.db = db

    def on_request(self):
        db = self.db
        user = db(db.users.user == Helper.get_user()).select().first()
        if user == None:
            redirect(URL('create_profile'))

    def transform(self, output, shared_data=None):
        if not isinstance(output, dict):
            return output

        output['admin'] = Helper.get_role() == 'Admin'
        output['approved'] = Helper.get_role() == 'Approved' or Helper.get_role() == 'Admin'

        return output
