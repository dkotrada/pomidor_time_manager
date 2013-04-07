# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Dieter Konrad dkotrada@gmail.com# This file is distributed under the license LGPL version 2 or later
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('pomidor')

import logging
logger = logging.getLogger('pomidor')

from pomidor_lib.AboutDialog import AboutDialog

# See pomidor_lib.AboutDialog.py for more details about how this class works.
class AboutPomidorDialog(AboutDialog):
    __gtype_name__ = "AboutPomidorDialog"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutPomidorDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

