# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
'''
# Copyright (C) <2013> <Dieter Konrad https://launchpad.net/~dkotrada>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
### END LICENSE

import gettext, os
from gettext import gettext as _
gettext.textdomain('pomidor')

from gi.repository import GLib, GObject, Unity, Notify, Dbusmenu # pylint: disable=E0611
import logging
logger = logging.getLogger('pomidor')

from pomidor_lib import Window
from pomidor.AboutPomidorDialog import AboutPomidorDialog
from pomidor.SettingsDialog import SettingsDialog

from pomidor import pycanberra

zeit_mark = "<span font_desc='59.0'>%02i:%02i</span>"

# See pomidor_lib.Window.py for more details about how this class works
class PomidorWindow(Window):
    __gtype_name__ = "PomidorWindow"

    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(PomidorWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutPomidorDialog
        self.SettingsDialog = SettingsDialog

        # Code for other initialization actions should be added here.
        self.initialize_quicklist()

        self.timeout_id = None
        self.time = 0
        self.minimizeonclicked = 1
        self.say = Salert()

        self.pbutton = self.builder.get_object("pbutton")
        self.sbutton = self.builder.get_object("sbutton")
        self.lbutton = self.builder.get_object("lbutton")
        self.timelabel = self.builder.get_object("timelabel")

        # Optionally play sound
        userpath = GLib.get_user_data_dir()
        fullpath = userpath + "/pomidor/config" # plus app path

        # run only once when window initialized
        if  os.path.exists(fullpath):
            pass
        else:
            print "No file. Create file now."
            #  set True by deafault is sound notification enabled
            content = True
            s = str(content)

            # create the filename
            title = "config"
            data_dir = GLib.get_user_data_dir()
            pomidor_dir = os.path.join(data_dir, "pomidor")
            filename = os.path.join(pomidor_dir, title)

            # write the data
            GLib.mkdir_with_parents(pomidor_dir, 0o700)
            GLib.file_set_contents(filename, s)


    def initialize_quicklist(self):
        """ Initialize a nice dynamic quicklist. """
        launcher = Unity.LauncherEntry.get_for_desktop_id("pomidor.desktop")
        quicklist = Dbusmenu.Menuitem.new()
        
        pitem = Dbusmenu.Menuitem.new()
        pitem.property_set(Dbusmenu.MENUITEM_PROP_LABEL, _("Start Pomodoro"))
        pitem.connect("item-activated", self.on_pitem_clicked, None)

        sitem = Dbusmenu.Menuitem.new()
        sitem.property_set(Dbusmenu.MENUITEM_PROP_LABEL, _("Short Break"))
        sitem.connect("item-activated", self.on_sitem_clicked, None)

        litem = Dbusmenu.Menuitem.new()
        litem.property_set(Dbusmenu.MENUITEM_PROP_LABEL, _("Long Break"))
        litem.connect("item-activated", self.on_litem_clicked, None)

        quicklist.child_append(pitem)
        quicklist.child_append(sitem)
        quicklist.child_append(litem)

        launcher.set_property("quicklist", quicklist)

    def on_pitem_clicked(self, widget, event, data = None):
        """ Run pomidor via quicklist """
        self.on_pbutton_clicked(widget)

    def on_sitem_clicked(self, widget, event, data = None):
        """ Run shortbreak via quicklist """
        self.on_sbutton_clicked(widget)

    def on_litem_clicked(self, widget, event, data = None):
        """ Run longbreak via quicklist """
        self.on_lbutton_clicked(widget)


    def on_pbutton_clicked(self, widget):
        ''' Run Pomodoro '''
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.timelabel.set_markup(zeit_mark % (25, 0))
        self.time = 25 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)


    def on_sbutton_clicked(self, widget):
        ''' Run Shortbreak'''
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.timelabel.set_markup(zeit_mark % (5, 0))
        self.time = 5 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)


    def on_lbutton_clicked(self, widget):
        ''' Run Longbreak '''
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.timelabel.set_markup(zeit_mark % (15, 0))
        self.time = 15 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)


    def minimize_to_launcher(self):
        if self.minimizeonclicked:
            self.iconify()
            self.minimizeonclicked = 0


    def count_down(self):
        if self.time == 0:
            GObject.source_remove(self.timeout_id)
            self.say.play() # play sound when CountDown is over
            return False
        else:
            self.time -= 1
            m, s = divmod(self.time, 60)
            h, m = divmod(m, 60)        
            self.timelabel.set_markup(zeit_mark % (m, s))
            # Minutes visible on Launcher icon using import Unity and LibUnity
            launcher = Unity.LauncherEntry.get_for_desktop_id ("pomidor.desktop")
            launcher.set_property("count", m + 1)
            launcher.set_property("count_visible", True)
            self.minimize_to_launcher()
            

            if m == 0 and s == 0:
                launcher.set_property("count_visible", False)
                self.present() # show the window when timer is up
                self.minimizeonclicked = 1 # alow minimizing when timer is activated

        return True 


class Salert():
    """ Show a notification using libnotify, and play a sound using pycanberra. """

    image = "file:///usr/share/pomidor/media/pomidor.svg"

    def __init__(self):
        """ Make sure Notify is initted """
        if not Notify.is_initted():
            Notify.init("Pomidor")


    def play(self):
        # Show notification // NOTE for translation _("Stirng")
        n = Notify.Notification.new(_("Pomidor Time Manager"), _("Time is up!"), self.image)
        if not n.show():
            raise Exception(_("Could not show notification..."))

        # Optionally play sound. File is created when window is initialized above
        userpath = GLib.get_user_data_dir()
        fullpath = userpath + "/pomidor/config" # plus app path
            

        try:
            success, text = GLib.file_get_contents(fullpath)
            if success and text == "True":
                canberra = pycanberra.Canberra()
                canberra.easy_play_sync("service-login")
                canberra.destroy()
            else:
                pass

        except Exception:
            print "There is no config file!"
