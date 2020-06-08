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
