# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
"""
The :mod:`ui` module provides standard UI components for OpenLP.
"""
import logging

from PyQt4 import QtGui

log = logging.getLogger(__name__)

def add_welcome_page(parent, image):
    """
    Generate an opening welcome page for a wizard using a provided image.

    ``image``
        A splash image for the wizard.
    """
    parent.welcomePage = QtGui.QWizardPage()
    parent.welcomePage.setPixmap(QtGui.QWizard.WatermarkPixmap,
        QtGui.QPixmap(image))
    parent.welcomePage.setObjectName(u'WelcomePage')
    parent.welcomeLayout = QtGui.QVBoxLayout(parent.welcomePage)
    parent.welcomeLayout.setObjectName(u'WelcomeLayout')
    parent.titleLabel = QtGui.QLabel(parent.welcomePage)
    parent.titleLabel.setObjectName(u'TitleLabel')
    parent.welcomeLayout.addWidget(parent.titleLabel)
    parent.welcomeLayout.addSpacing(40)
    parent.informationLabel = QtGui.QLabel(parent.welcomePage)
    parent.informationLabel.setWordWrap(True)
    parent.informationLabel.setObjectName(u'InformationLabel')
    parent.welcomeLayout.addWidget(parent.informationLabel)
    parent.welcomeLayout.addStretch()
    parent.addPage(parent.welcomePage)

def save_cancel_button_box(parent):
    """
    Return a standard dialog button box with save and cancel buttons.
    """
    button_box = QtGui.QDialogButtonBox(parent)
    button_box.setStandardButtons(
        QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Cancel)
    button_box.setObjectName(u'%sButtonBox' % parent)
    QtCore.QObject.connect(button_box, QtCore.SIGNAL(u'accepted()'),
        parent.accept)
    QtCore.QObject.connect(button_box, QtCore.SIGNAL(u'rejected()'),
        parent.reject)
    return button_box 
