"""Provide a tkinter widget for a text viewer popup window.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_extra_view
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvextraview.extra_view_locale import _
from nvextraview.platform.platform_settings import KEYS
from nvextraview.platform.platform_settings import PLATFORM
from nvlib.gui.contents_window.contents_viewer import ContentsViewer
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
        self.popup.protocol("WM_DELETE_WINDOW", self.on_close_viewer)
        if PLATFORM != 'win':
            self.popup.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)
        ContentsViewer.__init__(self, self.popup, model, view, controller)
        self._mdl.add_observer(self)
        self.refresh()
        self.isOpen = True
        self.pluginPrefs['is_open'] = True

    def on_close_viewer(self):
        self.pluginPrefs['is_open'] = False
        self.isOpen = False
        self.on_quit()

    def on_quit(self, event=None):
        self._mdl.delete_observer(self)
        self.pluginPrefs['window_geometry'] = self.popup.winfo_geometry()
        self.popup.destroy()
        self.show_contents_view()

    def refresh(self, *args, **kwargs):
        if self._mdl.novel is not None:
            self.popup.title(f'{self._mdl.novel.title} {_("by")} {self._mdl.novel.authorName}')
        else:
            self.popup.title('')
        super().refresh()

    def show_contents_view(self):
        if not self._ui.middleFrame.winfo_manager():
            self._ui.middleFrame.pack(after=self._ui.leftFrame, side='left', expand=False, fill='both')

