from py4web import action, URL, request, abort
from yatl.helpers import XML
from py4web.utils.url_signer import URLSigner
from py4web.core import Fixture

class TagEdit(Fixture):

    TAGEDIT = '<tagedit url="{url}" callback_url="{callback_url}"></tagedit>'

    def __init__(self, url, session, signer=None, db=None, auth=None):
        self.get_available_url = url + '/get_available'
        self.get_applied_url = url + '/get_applied'
        self.set_url = url + '/set'
        self.signer = signer or URLSigner(session)
        # Creates an action (an entry point for URL calls),
        # mapped to the api method, that can be used to request pages
        # for the table.
        self.__prerequisites__ = [session]
        args = list(filter(None, [session, db, auth, self.signer.verify()]))

        f = action.uses(*args)(self.get_available_tags)
        action(self.get_available_url + "/<id>", method=["GET"])(f)

        f = action.uses(*args)(self.get_applied_tags)
        action(self.get_applied_url + "/<id>", method=["GET"])(f)

        f = action.uses(*args)(self.set_tags)
        action(self.set_url + "/<id>", method=["POST"])(f)

    def __call__(self, id=None):
        """This method returns the element that can be included in the page.
        @param id: id of the file uploaded.  This can be useful if there are
        multiple instances of this form on the page."""
        return XML(TagEdit.TAGEDIT.format(
            get_available_url=URL(self.get_available_url, id, signer=self.signer),
            get_applied_url=URL(self.get_applied_url, id, signer=self.signer),
            callback_url=URL(self.set_url, id, signer=self.signer)))

    def get_available_tags():
        # TODO: Implementation for available tags is universal; goes here!
        return dict(tags=[])

    def get_applied_tags():
        return dict(tags=[])

    def set_tags():
        abort(code=500, text="Attempted to call set tags on a generic TagEdit component")
        return
