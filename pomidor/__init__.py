# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
'''
# Copyright (C) <2013> <Dieter Konrad https://launchpad.net/~dkotrada>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
### END LICENSE

import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('pomidor')

# Close the app correctly when terminated with ctrl+c, Gtk.main() 
# should take care of this, but currently it doesn't...
# Relevant bug: https://bugzilla.gnome.org/show_bug.cgi?id=622084
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

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
