"""A "detach text viewer" plugin for novelibre.

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
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
import webbrowser

from abc import ABC, abstractmethod



class SubController:

    def initialize_controller(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

    def disable_menu(self):
        pass

    def enable_menu(self):
        pass

    def lock(self):
        pass

    def on_close(self):
        pass

    def on_quit(self):
        pass

    def unlock(self):
        pass



class PluginBase(ABC, SubController):
    VERSION = ''
    API_VERSION = ''
    DESCRIPTION = ''
    URL = ''

    def __init__(self):
        self.filePath = None
        self.isActive = True
        self.isRejected = False

    @abstractmethod
    def install(self, model, view, controller):
        self.initialize_controller(model, view, controller)

import gettext
import locale
import os
import sys

LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('nv_extra_view', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

from pathlib import Path

import tkinter as tk


def set_icon(widget, icon='logo', path=None, default=True):
    if path is None:
        path = os.path.dirname(sys.argv[0])
        if not path:
            path = '.'
        path = f'{path}/icons'
    try:
        pic = tk.PhotoImage(file=f'{path}/{icon}.png')
        widget.iconphoto(default, pic)
    except:
        return False

    return True

from tkinter import ttk

from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def refresh(self):
        pass
from xml import sax


class ContentViewParser(sax.ContentHandler):
    BULLET = '•'

    def __init__(self):
        super().__init__()
        self.textTag = ''
        self.xmlTag = ''
        self.emTag = ''
        self.strongTag = ''
        self.commentTag = ''
        self.commentXmlTag = ''
        self.noteTag = ''
        self.noteXmlTag = ''
        self.showTags = None

        self.taggedText = None

        self._list = None
        self._comment = None
        self._note = None
        self._em = None
        self._strong = None

    def feed(self, xmlString):
        self.taggedText = []
        self._list = False
        self._comment = False
        self._note = False
        self._em = False
        self._strong = False
        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        tag = self.textTag
        if self._em:
            tag = self.emTag
        elif self._strong:
            tag = self.strongTag
        if self._comment:
            tag = self.commentTag
        elif self._note:
            tag = self.noteTag
        self.taggedText.append((content, tag))

    def endElement(self, name):
        tag = self.xmlTag
        suffix = ''
        if self._comment:
            tag = self.commentXmlTag
        elif self._note:
            tag = self.noteXmlTag
        if name == 'p' and not self._list:
            suffix = '\n'
        elif name == 'em':
            self._em = False
        elif name == 'strong':
            self._strong = False
        elif name in ('li', 'creator', 'date', 'note-citation'):
            suffix = '\n'
        elif name == 'ul':
            self._list = False
            if self.showTags:
                suffix = '\n'
        elif name == 'comment':
            self._comment = False
        elif name == 'note':
            self._note = False
        if self.showTags:
            self.taggedText.append((f'</{name}>{suffix}', tag))
        else:
            self.taggedText.append((suffix, tag))

    def startElement(self, name, attrs):
        attributes = ''
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            attributes = f'{attributes} {attrKey}="{attrValue}"'
        tag = self.xmlTag
        suffix = ''
        if name == 'em':
            self._em = True
        elif name == 'strong':
            self._strong = True
        elif name == 'ul':
            self._list = True
            if self.showTags:
                suffix = '\n'
        elif name == 'comment':
            self._comment = True
            suffix = '\n'
        elif name == 'note':
            self._note = True
            suffix = '\n'
        elif name == 'li' and not self.showTags:
            suffix = f'{self.BULLET} '
        if self._comment:
            tag = self.commentXmlTag
        elif self._note:
            tag = self.noteXmlTag
        if self.showTags:
            self.taggedText.append((f'<{name}{attributes}>{suffix}', tag))
        else:
            self.taggedText.append((suffix, tag))
from datetime import date
from datetime import time

import calendar

try:
    LOCALE_PATH
except NameError:
    locale.setlocale(locale.LC_TIME, "")
    LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
    try:
        CURRENT_LANGUAGE = locale.getlocale()[0][:2]
    except:
        CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
    try:
        t = gettext.translation('novelibre', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
        _ = t.gettext
    except:

        def _(message):
            return message

WEEKDAYS = calendar.day_name
MONTHS = calendar.month_name


ROOT_PREFIX = 'rt'
CHAPTER_PREFIX = 'ch'
PLOT_LINE_PREFIX = 'ac'
SECTION_PREFIX = 'sc'
PLOT_POINT_PREFIX = 'ap'
CHARACTER_PREFIX = 'cr'
LOCATION_PREFIX = 'lc'
ITEM_PREFIX = 'it'
PRJ_NOTE_PREFIX = 'pn'
CH_ROOT = f'{ROOT_PREFIX}{CHAPTER_PREFIX}'
PL_ROOT = f'{ROOT_PREFIX}{PLOT_LINE_PREFIX}'
CR_ROOT = f'{ROOT_PREFIX}{CHARACTER_PREFIX}'
LC_ROOT = f'{ROOT_PREFIX}{LOCATION_PREFIX}'
IT_ROOT = f'{ROOT_PREFIX}{ITEM_PREFIX}'
PN_ROOT = f'{ROOT_PREFIX}{PRJ_NOTE_PREFIX}'

BRF_SYNOPSIS_SUFFIX = '_brf_synopsis'
CHAPTERS_SUFFIX = '_chapters_tmp'
CHARACTER_REPORT_SUFFIX = '_character_report'
CHARACTERS_SUFFIX = '_characters_tmp'
CHARLIST_SUFFIX = '_charlist_tmp'
DATA_SUFFIX = '_data'
GRID_SUFFIX = '_grid_tmp'
ITEM_REPORT_SUFFIX = '_item_report'
ITEMLIST_SUFFIX = '_itemlist_tmp'
ITEMS_SUFFIX = '_items_tmp'
LOCATION_REPORT_SUFFIX = '_location_report'
LOCATIONS_SUFFIX = '_locations_tmp'
LOCLIST_SUFFIX = '_loclist_tmp'
MAJOR_MARKER = _('Major Character')
MANUSCRIPT_SUFFIX = '_manuscript_tmp'
MINOR_MARKER = _('Minor Character')
PARTS_SUFFIX = '_parts_tmp'
PLOTLIST_SUFFIX = '_plotlist'
PLOTLINES_SUFFIX = '_plotlines_tmp'
PROJECTNOTES_SUFFIX = '_projectnote_report'
PROOF_SUFFIX = '_proof_tmp'
SECTIONLIST_SUFFIX = '_sectionlist'
SECTIONS_SUFFIX = '_sections_tmp'
STAGES_SUFFIX = '_structure_tmp'
XREF_SUFFIX = '_xref'


class Error(Exception):
    pass


class Notification(Error):
    pass


def norm_path(path):
    if path is None:
        path = ''
    return os.path.normpath(path)


def string_to_list(text, divider=';'):
    elements = []
    try:
        tempList = text.split(divider)
        for element in tempList:
            element = element.strip()
            if element and not element in elements:
                elements.append(element)
        return elements

    except:
        return []


def list_to_string(elements, divider=';'):
    try:
        text = divider.join(elements)
        return text

    except:
        return ''


def intersection(elemList, refList):
    return [elem for elem in elemList if elem in refList]


def verified_date(dateStr):
    if dateStr is not None:
        date.fromisoformat(dateStr)
    return dateStr


def verified_int_string(intStr):
    if intStr is not None:
        int(intStr)
    return intStr


def verified_time(timeStr):
    if  timeStr is not None:
        time.fromisoformat(timeStr)
        while timeStr.count(':') < 2:
            timeStr = f'{timeStr}:00'
    return timeStr



class ContentsViewerCtrl(SubController):

    def initialize_controller(self, model, view, controller):
        super().initialize_controller(model, view, controller)

        self._contentParser = ContentViewParser()
        self._contentParser.xmlTag = self.XML_TAG
        self._contentParser.emTag = self.EM_TAG
        self._contentParser.strongTag = self.STRONG_TAG
        self._contentParser.commentTag = self.COMMENT_TAG
        self._contentParser.commentXmlTag = self.COMMENT_XML_TAG
        self._contentParser.noteTag = self.NOTE_TAG
        self._contentParser.noteXmlTag = self.NOTE_XML_TAG

    def _convert_from_novx(self, text, textTag):
        if not self.showMarkup.get():
            self._contentParser.showTags = False
        else:
            self._contentParser.showTags = True
        self._contentParser.textTag = textTag
        self._contentParser.feed(text)
        return self._contentParser.taggedText[1:-1]

    def get_tagged_text(self):

        taggedText = []
        for chId in self._mdl.novel.tree.get_children(CH_ROOT):
            chapter = self._mdl.novel.chapters[chId]
            taggedText.append(chId)
            if chapter.chLevel == 2:
                if chapter.chType == 0:
                    headingTag = self.H2_TAG
                else:
                    headingTag = self.H2_UNUSED_TAG
            else:
                if chapter.chType == 0:
                    headingTag = self.H1_TAG
                else:
                    headingTag = self.H1_UNUSED_TAG
            if chapter.title:
                heading = f'{chapter.title}\n'
            else:
                    heading = f"[{_('Unnamed')}]\n"
            taggedText.append((heading, headingTag))

            for scId in self._mdl.novel.tree.get_children(chId):
                section = self._mdl.novel.sections[scId]
                taggedText.append(scId)
                textTag = ''
                if section.scType == 3:
                    headingTag = self.STAGE2_TAG
                elif section.scType == 2:
                    headingTag = self.STAGE1_TAG
                elif section.scType == 0:
                    headingTag = self.H3_TAG
                else:
                    headingTag = self.H3_UNUSED_TAG
                    textTag = self.UNUSED_TAG
                if section.title:
                    heading = f'[{section.title}]\n'
                else:
                    heading = f"[{_('Unnamed')}]\n"
                taggedText.append((heading, headingTag))

                if section.sectionContent:
                    textTuples = self._convert_from_novx(section.sectionContent, textTag)
                    taggedText.extend(textTuples)

        if not taggedText:
            taggedText.append((f'({_("No text available")})', self.ITALIC_TAG))
        return taggedText

from tkinter import font as tkFont

from tkinter import font as tkFont
from tkinter import ttk


class RichTextTk(tk.Text):
    H1_TAG = 'h1'
    H2_TAG = 'h2'
    H3_TAG = 'h3'
    ITALIC_TAG = 'italic'
    BOLD_TAG = 'bold'
    CENTER_TAG = 'center'
    BULLET_TAG = 'bullet'

    H1_SIZE = 1.2
    H2_SIZE = 1.1
    H3_SIZE = 1.0
    H1_SPACING = 2
    H2_SPACING = 2
    H3_SPACING = 1.5
    CENTER_SPACING = 1.5

    def __init__(self, master=None, **kw):
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side='right', fill='y')

        kw.update({'yscrollcommand': self.vbar.set})
        tk.Text.__init__(self, self.frame, **kw)
        self.pack(side='left', fill='both', expand=True)
        self.vbar['command'] = self.yview

        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

        defaultFont = tkFont.nametofont(self.cget('font'))

        em = defaultFont.measure('m')
        defaultSize = defaultFont.cget('size')
        boldFont = tkFont.Font(**defaultFont.configure())
        italicFont = tkFont.Font(**defaultFont.configure())
        h1Font = tkFont.Font(**defaultFont.configure())
        h2Font = tkFont.Font(**defaultFont.configure())
        h3Font = tkFont.Font(**defaultFont.configure())

        boldFont.configure(weight='bold')
        italicFont.configure(slant='italic')
        h1Font.configure(size=int(defaultSize * self.H1_SIZE), weight='bold')
        h2Font.configure(size=int(defaultSize * self.H2_SIZE), weight='bold')
        h3Font.configure(size=int(defaultSize * self.H3_SIZE), slant='italic')

        self.tag_configure(self.BOLD_TAG, font=boldFont)
        self.tag_configure(self.ITALIC_TAG, font=italicFont)
        self.tag_configure(self.H1_TAG, font=h1Font, spacing3=defaultSize,
                           justify='center', spacing1=defaultSize * self.H1_SPACING)
        self.tag_configure(self.H2_TAG, font=h2Font, spacing3=defaultSize,
                           justify='center', spacing1=defaultSize * self.H2_SPACING)
        self.tag_configure(self.H3_TAG, font=h3Font, spacing3=defaultSize,
                           justify='center', spacing1=defaultSize * self.H3_SPACING)
        self.tag_configure(self.CENTER_TAG, justify='center', spacing1=defaultSize * self.CENTER_SPACING)

        lmargin2 = em + defaultFont.measure('\u2022 ')
        self.tag_configure(self.BULLET_TAG, lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f'\u2022 {text}', self.BULLET_TAG)


class RichTextNv(RichTextTk):
    H1_UNUSED_TAG = 'h1Unused'
    H2_UNUSED_TAG = 'h2Unused'
    H3_UNUSED_TAG = 'h3Unused'
    UNUSED_TAG = 'unused'
    STAGE1_TAG = 'stage1'
    STAGE2_TAG = 'stage2'
    XML_TAG = 'xmlTag'
    COMMENT_TAG = 'commentTag'
    COMMENT_XML_TAG = 'commentXmlTag'
    NOTE_TAG = 'noteTag'
    NOTE_XML_TAG = 'noteXmlTag'
    EM_TAG = 'emTag'
    STRONG_TAG = 'strongTag'

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                height=20,
                width=60,
                spacing1=10,
                spacing2=2,
                wrap='word',
                padx=10,
                bg=kwargs['color_text_bg'],
                fg=kwargs['color_text_fg'],
                )
        defaultFont = tkFont.nametofont(self.cget('font'))

        defaultSize = defaultFont.cget('size')
        boldFont = tkFont.Font(**defaultFont.configure())
        italicFont = tkFont.Font(**defaultFont.configure())
        h1Font = tkFont.Font(**defaultFont.configure())
        h2Font = tkFont.Font(**defaultFont.configure())
        h3Font = tkFont.Font(**defaultFont.configure())

        boldFont.configure(weight='bold')
        italicFont.configure(slant='italic')
        h1Font.configure(size=int(defaultSize * self.H1_SIZE),
                         weight='bold',
                         )
        h2Font.configure(size=int(defaultSize * self.H2_SIZE),
                         weight='bold',
                         )
        h3Font.configure(size=int(defaultSize * self.H3_SIZE),
                         slant='italic',
                         )
        self.tag_configure(self.XML_TAG,
                           foreground=kwargs['color_xml_tag'],
                           )
        self.tag_configure(self.EM_TAG,
                           font=italicFont,
                           )
        self.tag_configure(self.STRONG_TAG,
                           font=boldFont,
                           )
        self.tag_configure(self.COMMENT_TAG,
                           background=kwargs['color_comment_tag'],
                           )
        self.tag_configure(self.COMMENT_XML_TAG,
                           foreground=kwargs['color_xml_tag'],
                           background=kwargs['color_comment_tag'],
                           )
        self.tag_configure(self.NOTE_TAG,
                           background=kwargs['color_comment_tag'],
                           )
        self.tag_configure(self.NOTE_XML_TAG,
                           foreground=kwargs['color_xml_tag'],
                           background=kwargs['color_note_tag'],
                           )
        self.tag_configure(self.H1_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_chapter'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.H1_UNUSED_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.H2_TAG,
                           font=h2Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_chapter'],
                           justify='center',
                           spacing1=defaultSize * self.H2_SPACING,
                           )
        self.tag_configure(self.H2_UNUSED_TAG,
                           font=h2Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H2_SPACING,
                           )
        self.tag_configure(self.H3_UNUSED_TAG,
                           font=h3Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_unused'],
                           justify='center',
                           spacing1=defaultSize * self.H3_SPACING,
                           )
        self.tag_configure(self.UNUSED_TAG,
                           foreground=kwargs['color_unused'],
                           )
        self.tag_configure(self.STAGE1_TAG,
                           font=h1Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_stage'],
                           justify='center',
                           spacing1=defaultSize * self.H1_SPACING,
                           )
        self.tag_configure(self.STAGE2_TAG,
                           font=h3Font,
                           spacing3=defaultSize,
                           foreground=kwargs['color_stage'],
                           justify='center',
                           spacing1=defaultSize * self.H3_SPACING,
                           )

from datetime import date

prefs = {}
launchers = {}

HOME_URL = 'https://github.com/peter88213/novelibre/'


def datestr(isoDate):
    if prefs['localize_date']:
        return date.fromisoformat(isoDate).strftime("%x")
    else:
        return isoDate


def get_section_date_str(section):
    if prefs['localize_date']:
        return section.localeDate
    else:
        return section.date


def to_string(text):
    if text is None:
        return ''

    return str(text)



class ContentsViewer(RichTextNv, Observer, ContentsViewerCtrl):

    def __init__(self, parent, model, view, controller):
        super().__init__(parent, **prefs)
        self.initialize_controller(model, view, controller)

        self.pack(expand=True, fill='both')
        self.showMarkup = tk.BooleanVar(parent, value=prefs['show_markup'])
        ttk.Checkbutton(parent, text=_('Show markup'), variable=self.showMarkup).pack(anchor='w')
        self.showMarkup.trace('w', self.refresh)
        self._textMarks = {}
        self._index = '1.0'
        self._parent = parent

    def on_close(self):
        self.reset_view()

    def refresh(self, event=None, *args):
        if self._mdl.prjFile is None:
            return

        if self._parent.winfo_manager():
            self.view_text()
            try:
                super().see(self._index)
            except KeyError:
                pass

    def reset_view(self):
        self.config(state='normal')
        self.delete('1.0', 'end')
        self.config(state='disabled')

    def see(self, idStr):
        try:
            self._index = self._textMarks[idStr]
            super().see(self._index)
        except KeyError:
            pass

    def view_text(self):
        taggedText = self.get_tagged_text()
        self._textMarks = {}

        self.config(state='normal')
        self.delete('1.0', 'end')

        for entry in taggedText:
            if len(entry) == 2:
                text, tag = entry
                self.insert('end', text, tag)
            else:
                index = f"{self.count('1.0', 'end', 'lines')[0]}.0"
                self._textMarks[entry] = index
        self.config(state='disabled')

import platform



class GenericKeys:

    QUIT_PROGRAM = ('<Control-q>', f'{_("Ctrl")}-Q')


class MacKeys(GenericKeys):

    QUIT_PROGRAM = ('<Command-q>', 'Cmd-Q')



class WindowsKeys(GenericKeys):

    QUIT_PROGRAM = ('<Alt-F4>', 'Alt-F4')


if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = GenericKeys()
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
else:
    PLATFORM = ''
    KEYS = GenericKeys()



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
        self.on_quit()

    def on_quit(self):
        if self.progressView is not None:
            if self.progressView.isOpen:
                self.progressView.on_quit()

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
        if self._ui.middleFrame.winfo_manager():
            self._ui.middleFrame.pack_forget()



class Plugin(PluginBase):
    VERSION = '0.1.0'
    API_VERSION = '5.0'
    DESCRIPTION = 'Text viewer popup'
    URL = 'https://github.com/peter88213/nv_extra_view'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_extra_view'

    FEATURE = _('Detach text viewer')

    def install(self, model, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.progressService = ExtraViewService(model, view, controller)

        self._ui.helpMenu.add_command(label=_('Progress viewer Online help'), command=self.open_help)

        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self.start_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE)

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.progressService.on_close()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        self.progressService.on_quit()

    def open_help(self, event=None):
        webbrowser.open(self.HELP_URL)

    def start_viewer(self):
        self.progressService.start_viewer(self.FEATURE)

