# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Dieter Konrad dkotrada@gmail.com# This file is distributed under the license LGPL version 2 or later
### END LICENSE

from gi.repository import Gio, Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('pomidor_lib')

from . helpers import get_builder, show_uri, get_help_uri

# This class is meant to be subclassed by PomidorWindow.  It provides
# common functions and some boilerplate.
class Window(Gtk.Window):
    __gtype_name__ = "Window"

    # To construct a new instance of this method, the following notable 
    # methods are called in this order:
    # __new__(cls)
    # __init__(self)
    # finish_initializing(self, builder)
    # __init__(self)
    #
    # For this reason, it's recommended you leave __init__ empty and put
    # your initialization code in finish_initializing
    
    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated BasePomidorWindow object.
        """
        builder = get_builder('PomidorWindow')
        new_object = builder.get_object("pomidor_window")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initializing should be called after parsing the UI definition
        and creating a PomidorWindow object with it in order to finish
        initializing the start of the new PomidorWindow instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self, True)
        self.AboutDialog = None # class
        self.SettingsDialog = None


    def on_help_clicked(self, widget, data=None):
        show_uri(self, "ghelp:%s" % get_help_uri())


    def on_info_clicked(self, widget, data=None):
        """Display the about box for pomidor."""
        if self.AboutDialog is not None:
            about = self.AboutDialog() # pylint: disable=E1102
            response = about.run()
            about.destroy()


    def on_settings_clicked(self, widget, data=None):
        """Display the settings dialog for pomidor."""
        if self.SettingsDialog is not None:
            settings = self.SettingsDialog() # pylint: disable=E1102
            response = settings.run()
            settings.destroy()


    def on_mnu_close_activate(self, widget, data=None):
        """Signal handler for closing the PomidorWindow."""
        self.destroy()


    def on_destroy(self, widget, data=None):
        """Called when the PomidorWindow is closed."""
        # Clean up code for saving application state should be added here.
        Gtk.main_quit()
