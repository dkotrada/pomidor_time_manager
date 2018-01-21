# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
'''
# Copyright (C) <2013> <Dieter Konrad https://launchpad.net/~dkotrada>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
### END LICENSE

from gi.repository import Gtk, GLib # pylint: disable=E0611

from pomidor_lib.helpers import get_builder

import gettext, os
from gettext import gettext as _
gettext.textdomain('pomidor')

class SettingsDialog(Gtk.Dialog):
    __gtype_name__ = "SettingsDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated SettingsDialog object.
        """
        builder = get_builder('SettingsDialog')
        new_object = builder.get_object('settings_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a SettingsDialog object with it in order to
        finish initializing the start of the new SettingsDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

        self.check = self.builder.get_object('checkbutton_sound')

        # Write the file first time
        userpath = GLib.get_user_data_dir()
        fullpath = userpath + "/pomidor/config"   


        # read file and set False or True to self.check.set_active() 
        # try to get the data from the file if it exists
        try:
            success, text = GLib.file_get_contents(fullpath)
            if success and text == "True":
                self.check.set_active(True)
            else:
                self.check.set_active(False)

        except Exception:
            print "There is no file!"
            

    def on_checkbutton_sound_toggled(self, widget, data=None):
        if self.check.get_active():
            # write the string True to file
            content = True
            s = str(content)

            # create file the filename
            title = "config"
            data_dir = GLib.get_user_data_dir()
            pomidor_dir = os.path.join(data_dir, "pomidor")
            filename = os.path.join(pomidor_dir, title)
            
            # write the data
            GLib.mkdir_with_parents(pomidor_dir, 0o700)
            GLib.file_set_contents(filename, s)
        else:
            # write the string False to file
            content = False
            s = str(content)

            # create file the filename
            title = "config"
            data_dir = GLib.get_user_data_dir()
            pomidor_dir = os.path.join(data_dir, "pomidor")
            filename = os.path.join(pomidor_dir, title)
            
            # write the data
            GLib.mkdir_with_parents(pomidor_dir, 0o700)
            GLib.file_set_contents(filename, s)

    def on_btn_ok_clicked(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns Gtk.ResponseType.OK from run().
        """
        pass



if __name__ == "__main__":
    dialog = SettingsDialog()
    dialog.show()
    Gtk.main()
