# components/__init__.py - init for components
# part of Sluggo, a free and open source issue tracker
# Copyright (c) 2020 Slugbotics - see git repository history for individual committers
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from .validUser import UserValidator
from .comment import Comment
from ..common import db, session, T, cache, auth, signed_url

comments = Comment("comment", session, signer=signed_url, db=db, auth=auth)
userValidator = UserValidator(db)
