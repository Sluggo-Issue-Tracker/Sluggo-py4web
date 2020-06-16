# tasks.py - probably unused file
# part of Sluggo, a free and open source issue tracker
# Copyright (c) 2020 Slugbotics - see git repository history for individual committers
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

"""
To use celery tasks:
1) pip install -U "celery[redis]" 
2) In settings.py: 
   USE_CELERY = True
   CELERY_BROKER = "redis://localhost:6379/0"
3) Start "redis-server"
4) Start "celery -A apps.{appname}.tasks beat"
5) Start "celery -A apps.{appname}.tasks worker --loglevel=info" for each worker

"""
from .common import settings, scheduler, db, Field

# example of task that needs db access
@scheduler.task
def my_task():
    try:
        # this task will be executed in its own thread, connect to db
        db._adapter.reconnect()
        # do something here
        db.commit()
    except:
        # rollback on failure
        db.rollback()


# run my_task very 10 seconds
scheduler.conf.beat_schedule = {
    "my_first_task": {
        "task": "apps.%s.tasks.my_task" % settings.APP_NAME,
        "schedule": 10.0,
        "args": (),
    },
}
