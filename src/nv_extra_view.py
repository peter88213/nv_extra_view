"""A "detach text viewer" plugin for novelibre.

Requires Python 3.6+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_extra_view
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from nvlib.controller.plugin.plugin_base import PluginBase
from nvextraview.extra_view_locale import _
from nvextraview.extra_view_service import ExtraViewService


class Plugin(PluginBase):
    """novelibre detach text viewer plugin class."""
    VERSION = '@release'
    API_VERSION = '5.6'
    DESCRIPTION = 'Text viewer popup'
    URL = 'https://github.com/peter88213/nv_extra_view'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_extra_view'

    FEATURE = _('Detach text viewer')

    def install(self, model, view, controller):
        """Extend the 'View' menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.extraViewService = ExtraViewService(model, view, controller)

        # Create an entry in the View menu.
        pos = self._ui.viewMenu.index(_('Detach/Dock Properties')) + 1
        self._ui.viewMenu.insert_command(pos, label=self.FEATURE, command=self.start_viewer)
        self._ui.viewMenu.entryconfig(self.FEATURE)

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.extraViewService.on_close()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        self.extraViewService.on_quit()

    def start_viewer(self):
        self.extraViewService.start_viewer()

