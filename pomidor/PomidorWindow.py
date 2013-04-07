# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Dieter Konrad dkotrada@gmail.com# This file is distributed under the license LGPL version 2 or later
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('pomidor')

from gi.repository import Gtk, GObject # pylint: disable=E0611
import logging
logger = logging.getLogger('pomidor')

from pomidor_lib import Window
from pomidor.AboutPomidorDialog import AboutPomidorDialog
#from pomidor.PreferencesPomidorDialog import PreferencesPomidorDialog

from pomidor import pycanberra
import subprocess

ZEIT = "<span font_desc=\"59.0\">%02i:%02i</span>"

# See pomidor_lib.Window.py for more details about how this class works
class PomidorWindow(Window):
    __gtype_name__ = "PomidorWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(PomidorWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutPomidorDialog
        #self.PreferencesDialog = PreferencesPomidorDialog

        # Code for other initialization actions should be added here.

        self.timeout_id = None
        self.time = 0
        self.say = Salert()

        self.pbutton = self.builder.get_object("pbutton")
        self.sbutton = self.builder.get_object("sbutton")
        self.lbutton = self.builder.get_object("lbutton")
        self.timelabel = self.builder.get_object("timelabel")


    def on_pbutton_clicked(self, widget):
        ''' Run Pomodoro '''
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.timelabel.set_markup(ZEIT % (25, 0))
        self.time = 25 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)


    def on_sbutton_clicked(self, widget):
        ''' Run Shortbreak'''
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.timelabel.set_markup(ZEIT % (5, 0))
        self.time = 5 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)


    def on_lbutton_clicked(self, widget):
        ''' Run Longbreak '''
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.timelabel.set_markup(ZEIT % (15, 0))
        self.time = 15 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)


    def count_down(self):
        if self.time == 0:
            GObject.source_remove(self.timeout_id)
            self.say.play() # play sound when CountDown is over
            return False
        else:
            self.time -= 1
            m, s = divmod(self.time, 60)
            h, m = divmod(m, 60)        
            self.timelabel.set_markup(ZEIT % (m, s))
        return True


class Salert():

    def play(self):
        # Message
        subprocess.Popen("notify-send -i /usr/share/pomidor/media/pomidor.svg 'Pomidor Time Manager' 'Time is up!'", shell=True)
        # Sound
        canberra = pycanberra.Canberra()
        canberra.easy_play_sync("service-login")
        canberra.destroy()
