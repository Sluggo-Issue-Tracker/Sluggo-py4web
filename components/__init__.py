from .validUser import UserValidator
from .comment import Comment
from ..common import db, session, T, cache, auth, signed_url

comments = Comment("comment", session, signer=signed_url, db=db, auth=auth)
userValidator = UserValidator(db)
