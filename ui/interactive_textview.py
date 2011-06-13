#!/usr/bin/python

#       interactive_textview.py
#       
#       Copyright 2011 Hugo Teso <hugo.teso@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os

import gtk, pango
import gtksourceview2

import ui.interactive_buttons as interactive_buttons

class InteractiveTextView(gtk.VBox):
    '''Interactive Right TextView elements'''

    def __init__(self, uicore):
        super(InteractiveTextView,self).__init__(False, 1)

        self.uicore = uicore

        #################################################################
        # Interactive Right Textview
        #################################################################

        # Use GtkSourceView to add eye candy :P
        # create buffer
        lm = gtksourceview2.LanguageManager()
        # Add ui dir to language paths
        paths = lm.get_search_path()
        paths.append(os.getcwd() + os.sep + 'ui' + os.sep + 'data' + os.sep)
        lm.set_search_path(paths)
        self.buffer = gtksourceview2.Buffer()
        self.buffer.create_tag("green-background", background="green", foreground="black")
        self.buffer.set_data('languages-manager', lm)
        self.view = gtksourceview2.View(self.buffer)

        # FIXME options must be user selectable (statusbar)
        self.view.set_editable(False)
        self.view.set_highlight_current_line(True)
        # posible values: gtk.WRAP_NONE, gtk.WRAP_CHAR, gtk.WRAP_WORD...
        self.view.set_wrap_mode(gtk.WRAP_NONE)
        
        # setup view
        font_desc = pango.FontDescription('monospace 9')
        if font_desc:
            self.view.modify_font(font_desc)

        self.buffer.set_highlight_syntax(True)
        manager = self.buffer.get_data('languages-manager')
        language = manager.get_language('asm')
        self.buffer.set_language(language)

        self.mgr = gtksourceview2.style_scheme_manager_get_default()

        # Scrolled Window
        self.interactive_scrolled_window = gtk.ScrolledWindow()
        self.interactive_scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.interactive_scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.interactive_scrolled_window.show()
        # Add Textview to Scrolled Window
        self.interactive_scrolled_window.add(self.view)
        self.pack_start(self.interactive_scrolled_window, expand=True, fill=True)

        # Interactive buttons
        self.interactive_buttons = interactive_buttons.InteractiveButtons(self.uicore, self.buffer)
        self.pack_end(self.interactive_buttons, expand=False, fill=True)

        # Add hexdump to textview
        self.uicore.pyew.offset = 0
        dump = self.uicore.pyew.hexdump(self.uicore.pyew.buf, self.uicore.pyew.hexcolumns)
        self.buffer.set_text(dump)
