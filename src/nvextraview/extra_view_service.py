"""Provide a service class for the extra viewer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_extra_view
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from mvclib.controller.sub_controller import SubController
from mvclib.view.set_icon_tk import set_icon
from nvextraview.extra_view import ExtraView


class ExtraViewService(SubController):
    INI_FILENAME = 'extra_view.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        window_geometry='400x640',
    )
    OPTIONS = dict(
        show_markup=False,
    )

    def __init__(self, model, view, controller):
        super().initialize_controller(model, view, controller)
        self.progressView = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.prefs = {}
        self.prefs.update(self.configuration.settings)
        self.prefs.update(self.configuration.options)

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.on_quit()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        if self.progressView is not None:
            if self.progressView.isOpen:
                self.progressView.on_quit()

        #--- Save configuration
        for keyword in self.prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.prefs[keyword]
        self.configuration.write(self.iniFile)

    def start_viewer(self, windowTitle):
        self.hide_contents_view()
        if self.progressView:
            if self.progressView.isOpen:
                if self.progressView.popup.state() == 'iconic':
                    self.progressView.popup.state('normal')
                self.progressView.popup.lift()
                self.progressView.popup.focus()
                return

        self.progressView = ExtraView(self._mdl, self._ui, self._ctrl, self.prefs)
        self.progressView.popup.title(f'{self._mdl.novel.title} - {windowTitle}')
        set_icon(self.progressView.popup, icon='wLogo32', default=False)

    def hide_contents_view(self):
        """Show/hide the contents viewer text box."""
        if self._ui.middleFrame.winfo_manager():
            self._ui.middleFrame.pack_forget()

