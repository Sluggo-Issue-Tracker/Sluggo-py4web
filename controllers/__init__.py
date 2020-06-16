# controllers/__init__.py - init code for controllers
# part of Sluggo, a free and open source issue tracker
# Copyright (c) 2020 Slugbotics - see git repository history for individual committers
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

# this initializes controllers directory
# check that sweet compatibility
import py4web

assert py4web.check_compatible("0.1.20190709.1")

from . import tickets, users, index, admin, help

# optional parameters
__version__ = "0.0.0"
__author__ = "you <you@example.com>"
__license__ = "anything you want"
