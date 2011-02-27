# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import logging

from PyQt4 import QtCore, QtGui

from firsttimewizard import Ui_FirstTimeWizard

from openlp.core.lib import translate, PluginStatus
from openlp.core.utils import get_web_page, LanguageManager

log = logging.getLogger(__name__)

class FirstTimeForm(QtGui.QWizard, Ui_FirstTimeWizard):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of
    OpenLP themes.
    """
    log.info(u'ThemeWizardForm loaded')

    def __init__(self, parent=None):
        # check to see if we have web access
        self.webAccess = get_web_page(u'http://openlp.org/files/frw/themes.lst')
        print self.webAccess
        if self.webAccess:
            self.themes = self.webAccess.read()
            songs = get_web_page(u'http://openlp.org/files/frw/songs.lst')
            self.songs = songs.read()
            bibles = get_web_page(u'http://openlp.org/files/frw/bibles.lst')
            self.bibles = bibles.read()
        QtGui.QWizard.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.autoLanguageCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onAutoLanguageClicked)
        #self.registerFields()

    def exec_(self, edit=False):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def setDefaults(self):
        """
        Set up display at start of theme edit.
        """
        self.restart()
        # Sort out internet access for downloads
        if self.webAccess:
            self.internetGroupBox.setVisible(True)
            self.noInternetLabel.setVisible(False)
        else:
            self.internetGroupBox.setVisible(False)
            self.noInternetLabel.setVisible(True)
        # Sort out Language settings
        self.autoLanguageCheckBox.setChecked(True)
        self.LanguageComboBox.setEnabled(False)
        self.qmList = LanguageManager.get_qm_list()
        for key in sorted(self.qmList.keys()):
            self.LanguageComboBox.addItem(key)
        treewidgetitem = QtGui.QTreeWidgetItem(self.selectionTreeWidget)
        treewidgetitem.setText(0, u'Songs')
        self.__loadChild(treewidgetitem, self.songs)
        treewidgetitem = QtGui.QTreeWidgetItem(self.selectionTreeWidget)
        treewidgetitem.setText(0, u'Bibles')
        self.__loadChild(treewidgetitem, self.bibles)
        treewidgetitem = QtGui.QTreeWidgetItem(self.selectionTreeWidget)
        treewidgetitem.setText(0, u'Themes')
        self.__loadChild(treewidgetitem, self.themes)

    def __loadChild(self, tree, list):
        list = list.split(u'\n')
        for item in list:
            if item:
                child = QtGui.QTreeWidgetItem(tree)
                child.setText(0, item)
                child.setCheckState(0, QtCore.Qt.Unchecked)
                child.setFlags(QtCore.Qt.ItemIsUserCheckable |
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            #self.themeSelectionComboBox.addItem(theme)

    def accept(self):
        self.__pluginStatus(self.songsCheckBox, u'songs/status')
        self.__pluginStatus(self.bibleCheckBox, u'bibles/status')
        self.__pluginStatus(self.presentationCheckBox, u'presentations/status')
        self.__pluginStatus(self.imageCheckBox, u'images/status')
        self.__pluginStatus(self.mediaCheckBox, u'media/status')
        self.__pluginStatus(self.remoteCheckBox, u'remotes/status')
        self.__pluginStatus(self.customCheckBox, u'custom/status')
        self.__pluginStatus(self.songUsageCheckBox, u'songusage/status')
        self.__pluginStatus(self.alertCheckBox, u'alerts/status')
        if self.autoLanguageCheckBox.checkState() == QtCore.Qt.Checked:
            LanguageManager.auto_language = True
            LanguageManager.set_language(False, False)
        else:
            LanguageManager.auto_language = False
            action = QtGui.QAction(None)
            action.setObjectName(unicode(self.LanguageComboBox.currentText()))
            LanguageManager.set_language(action, False)
        return QtGui.QWizard.accept(self)

    def onAutoLanguageClicked(self, state):
        if state == QtCore.Qt.Checked:
            self.LanguageComboBox.setEnabled(False)
        else:
            self.LanguageComboBox.setEnabled(True)

    def __pluginStatus(self, field, tag):
        status = PluginStatus.Active if field.checkState() \
            == QtCore.Qt.Checked else PluginStatus.Inactive
        QtCore.QSettings().setValue(tag, QtCore.QVariant(status))
