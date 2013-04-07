# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Dieter Konrad dkotrada@gmail.com# This file is distributed under the license LGPL version 2 or later
### END LICENSE

import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('pomidor')

from gi.repository import Gtk # pylint: disable=E0611

from pomidor import PomidorWindow

from pomidor_lib import set_up_logging, get_version

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs pomidor_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

def main():
    'constructor for your class instances'
    parse_options()

    # Run the application.    
    window = PomidorWindow.PomidorWindow()
    window.show()
    Gtk.main()
