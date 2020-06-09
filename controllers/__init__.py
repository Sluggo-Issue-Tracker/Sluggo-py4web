# this initializes controllers directory
# check that sweet compatibility
import py4web

assert py4web.check_compatible("0.1.20190709.1")

from . import tickets, users, index, admin, help

# optional parameters
__version__ = "0.0.0"
__author__ = "you <you@example.com>"
__license__ = "anything you want"
