"""Provide a tkinter widget for a text viewer popup window.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_extra_view
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.contents_window.contents_viewer import ContentsViewer
from nvextraview.platform.platform_settings import KEYS
from nvextraview.platform.platform_settings import PLATFORM
import tkinter as tk


class ExtraView(ContentsViewer):

    def __init__(self, model, view, controller, prefs):
        self._mdl = model
        self._ctrl = controller
        self.popup = tk.Toplevel()
        self.prefs = self._ctrl.get_preferences()
        self.pluginPrefs = prefs
        self.popup.geometry(self.pluginPrefs['window_geometry'])
        self.popup.lift()
        self.popup.focus()
        self.popup.protocol("WM_DELETE_WINDOW", self.on_quit)
        if PLATFORM != 'win':
            self.popup.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)
        ContentsViewer.__init__(self, self.popup, model, view, controller)
        self._mdl.add_observer(self)
        self.refresh()
        self.isOpen = True

    def on_quit(self, event=None):
        self._mdl.delete_observer(self)
        self.pluginPrefs['window_geometry'] = self.popup.winfo_geometry()
        self.popup.destroy()
        self.isOpen = False
        self.show_contents_view()

    def show_contents_view(self):
        if not self._ui.middleFrame.winfo_manager():
            self._ui.middleFrame.pack(after=self._ui.leftFrame, side='left', expand=False, fill='both')

