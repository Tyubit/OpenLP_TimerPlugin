# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import logging

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from openlp.core.resources import *
from openlp.core.lib import Plugin, PluginUtils

from openlp.plugins.bibles.lib import BibleManager, BiblesTab, BibleMediaItem
from openlp.plugins.bibles.lib.tables import *
from openlp.plugins.bibles.lib.classes import *

class BiblePlugin(Plugin, PluginUtils):
    global log
    log=logging.getLogger("BiblePlugin")
    log.info("Bible Plugin loaded")

    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Bible', '1.9.0')
        self.weight = -9
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_verse.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #Register the bible Manager
        self.biblemanager = BibleManager(self.config)

    def get_settings_tab(self):
        self.BiblesTab = BiblesTab()
        return self.BiblesTab

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        self.media_item = BibleMediaItem(self, self.icon, 'Bible Verses')
        return self.media_item

    def add_import_menu_item(self, import_menu):
        self.ImportBibleItem = QtGui.QAction(import_menu)
        self.ImportBibleItem.setObjectName("ImportBibleItem")
        import_menu.addAction(self.ImportBibleItem)
        self.ImportBibleItem.setText(QtGui.QApplication.translate("main_window", "&Bible", None, QtGui.QApplication.UnicodeUTF8))
        # Signals and slots
        QtCore.QObject.connect(self.ImportBibleItem, QtCore.SIGNAL("triggered()"),  self.onBibleNewClick)

    def add_export_menu_item(self, export_menu):
        self.ExportBibleItem = QtGui.QAction(export_menu)
        self.ExportBibleItem.setObjectName("ExportBibleItem")
        export_menu.addAction(self.ExportBibleItem)
        self.ExportBibleItem.setText(QtGui.QApplication.translate("main_window", "&Bible", None, QtGui.QApplication.UnicodeUTF8))

    def initialise(self):
        pass

    def onBibleNewClick(self):
        self.bibleimportform = BibleImportForm(self.config, self.biblemanager, self)
        self.bibleimportform.exec_()
        pass

    def load_settings(self):
        pass
#        self.SettingsOutputStyleComboBox.setCurrentIndex(int(self.config.get_config("bible_output_style", 0)))
#        self.SettingsVerseStyleComboBox.setCurrentIndex(int(self.config.get_config("bible_verse_style", 0)))
#        try:
#            self.SettingsNewChapterCheck.setCheckState(int(self.config.get_config("bible_new_chapter", 0)))
#        except:
#            pass

    def save_settings(self):
        pass
#        self.config.set_config("bible_output_style", str(self.SettingsOutputStyleComboBox.currentIndex()))
#        self.config.set_config("bible_verse_style", str(self.SettingsVerseStyleComboBox.currentIndex()))
#        self.config.set_config("bible_new_chapter", str(self.SettingsNewChapterCheck.checkState()))

#        self.SettingsOutputStyleComboBox.clear()
#       self.SettingsVerseStyleComboBox.clear()

#        self.SettingsOutputStyleComboBox.addItem(u"Continuous")
#        self.SettingsOutputStyleComboBox.addItem(u"Paragraph")
#        self.SettingsVerseStyleComboBox.addItem(u"No Brackets")
#        self.SettingsVerseStyleComboBox.addItem(u"( and )")
#        self.SettingsVerseStyleComboBox.addItem(u"{ and }")
#        self.SettingsVerseStyleComboBox.addItem(u"[ and ]")


    def define_tab(self):
        pass
#        QtCore.QObject.connect(self.SettingsResetButton, QtCore.SIGNAL("pressed()"), self.onSettingsResetButton)
#        QtCore.QObject.connect(self.SettingsSaveButton, QtCore.SIGNAL("pressed()"), self.onSettingsSaveButton)
