# controllers.py - mockup controller for use in py4web
# Copyright (c) 2020 Andrew Gavgavian, Samuel Schmidt, and Isaac
# Trimble-Pederson, All Rights Reserved

from py4web.core import action

@action("index")
@action.uses("index.html")
def index():
    return dict()


@action('users')
@action.uses('users.html')
def add_contacts():
    return dict()

@action('ticketmock')
@action.uses('ticketmock.html')
def ticketmock():
    return dict()

@action('hpmock')
@action.uses('hpmock.html')
def homemock():
    return dict()
