# test_data.py - various test data
# part of Sluggo, a free and open source issue tracker
# Copyright (c) 2020 Slugbotics - see git repository history for individual committers
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

# Test code that doesn't work in isolation
# Testing user sorting

# Mock / debug code for testing user sort
# In a perfect world this would be factored out to an automated test
newAdmins = [
    dict(
        auth_user=dict(
            first_name="Isaac",
            last_name="Trimble-Pederson"
        )
    ),
    dict(
        auth_user=dict(
            first_name="Theo",
            last_name="Kell"
        )
    ),
    dict(
        auth_user=dict(
            first_name="Andrew",
            last_name="Gavgavian"
        )
    ),
    dict(
        auth_user=dict(
            first_name="Jacob",
            last_name="Ross"
        )
    ),
    dict(
        auth_user=dict(
            first_name="Wren",
            last_name="Sakai"
        )
    )
]

