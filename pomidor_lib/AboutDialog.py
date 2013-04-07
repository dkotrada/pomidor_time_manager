# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Dieter Konrad dkotrada@gmail.com# This file is distributed under the license LGPL version 2 or later
### END LICENSE

from gi.repository import Gtk # pylint: disable=E0611

from . helpers import get_builder

class AboutDialog(Gtk.AboutDialog):
    __gtype_name__ = "AboutDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated AboutDialog object.
        """
        builder = get_builder('AboutPomidorDialog')
        new_object = builder.get_object("about_pomidor_dialog")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initalizing should be called after parsing the ui definition
        and creating a AboutDialog object with it in order
        to finish initializing the start of the new AboutPomidorDialog
        instance.
        
        Put your initialization code in here and leave __init__ undefined.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

