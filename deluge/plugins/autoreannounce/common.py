#
# -*- coding: utf-8 -*-#

# Copyright (C) 2016 Joel Elkins <joel@elkins.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
# Copyright (C) 2010 Pedro Algarvio <pedro@algarvio.me>
#
# This file is part of AutoReannounce and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#


def get_resource(filename):
    import pkg_resources
    import os
    return pkg_resources.resource_filename("deluge.plugins.autoreannounce",
                                           os.path.join("data", filename))
