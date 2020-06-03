"""
this component serves to provide comment functionality
"""

from py4web import action, URL, request
from yatl.helpers import XML
from py4web.utils.url_signer import URLSigner
from py4web.core import Fixture


class Comment(Fixture):
    COMMENT = '<comment comment_id="{id}"></comment>'

    def __init__(self, url, ticket):
        self.url = url
        self.ticket = ticket
