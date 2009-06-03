# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'authorsdialog.ui'
#
# Created: Sat Jan  3 11:48:36 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from openlp.plugins.songs.lib import TextListData

class Ui_AuthorsDialog(object):
    def setupUi(self, AuthorsDialog):
        AuthorsDialog.setObjectName("AuthorsDialog")
        AuthorsDialog.resize(410, 505)
        self.DialogLayout = QtGui.QVBoxLayout(AuthorsDialog)
        self.DialogLayout.setSpacing(8)
        self.DialogLayout.setMargin(8)
        self.DialogLayout.setObjectName("DialogLayout")


#        self.AuthorListView = QtGui.QTableWidget(AuthorsDialog)
#        self.AuthorListView.setDragEnabled(True)
#        self.AuthorListView.setAlternatingRowColors(True)
#        self.AuthorListView.setColumnCount(0)
#        self.AuthorListView.setObjectName("AuthorListView")
#        self.AuthorListView.setColumnCount(0)
#        self.AuthorListView.setRowCount(0)
        self.AuthorListView = QtGui.QListView()
        self.AuthorListView.setAlternatingRowColors(True)
        self.AuthorListData = TextListData()
        self.AuthorListView.setModel(self.AuthorListData)
        self.DialogLayout.addWidget(self.AuthorListView)

        self.AuthorDetails = QtGui.QGroupBox(AuthorsDialog)
        self.AuthorDetails.setMinimumSize(QtCore.QSize(0, 0))
        self.AuthorDetails.setObjectName("AuthorDetails")
        self.AuthorLayout = QtGui.QVBoxLayout(self.AuthorDetails)
        self.AuthorLayout.setSpacing(8)
        self.AuthorLayout.setMargin(8)
        self.AuthorLayout.setObjectName("AuthorLayout")
        self.DetailsWidget = QtGui.QWidget(self.AuthorDetails)
        self.DetailsWidget.setObjectName("DetailsWidget")
        self.DetailsLayout = QtGui.QFormLayout(self.DetailsWidget)
        self.DetailsLayout.setMargin(0)
        self.DetailsLayout.setSpacing(8)
        self.DetailsLayout.setObjectName("DetailsLayout")
        self.DisplayLabel = QtGui.QLabel(self.DetailsWidget)
        self.DisplayLabel.setObjectName("DisplayLabel")
        self.DetailsLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.DisplayLabel)
        self.DisplayEdit = QtGui.QLineEdit(self.DetailsWidget)
        self.DisplayEdit.setObjectName("DisplayEdit")
        self.DetailsLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.DisplayEdit)
        self.FirstNameLabel = QtGui.QLabel(self.DetailsWidget)
        self.FirstNameLabel.setObjectName("FirstNameLabel")
        self.DetailsLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.FirstNameLabel)
        self.FirstNameEdit = QtGui.QLineEdit(self.DetailsWidget)
        self.FirstNameEdit.setObjectName("FirstNameEdit")
        self.DetailsLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.FirstNameEdit)
        self.LastNameLabel = QtGui.QLabel(self.DetailsWidget)
        self.LastNameLabel.setObjectName("LastNameLabel")
        self.DetailsLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.LastNameLabel)
        self.LastNameEdit = QtGui.QLineEdit(self.DetailsWidget)
        self.LastNameEdit.setObjectName("LastNameEdit")
        self.DetailsLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.LastNameEdit)
        self.AuthorLayout.addWidget(self.DetailsWidget)
        self.MessageLabel = QtGui.QLabel(self.AuthorDetails)
        self.MessageLabel.setObjectName("MessageLabel")
        self.AuthorLayout.addWidget(self.MessageLabel)
        self.ButtonWidget = QtGui.QWidget(self.AuthorDetails)
        self.ButtonWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.ButtonWidget.setObjectName("ButtonWidget")
        self.ButtonLayout = QtGui.QHBoxLayout(self.ButtonWidget)
        self.ButtonLayout.setSpacing(8)
        self.ButtonLayout.setMargin(0)
        self.ButtonLayout.setObjectName("ButtonLayout")
        spacerItem = QtGui.QSpacerItem(198, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ButtonLayout.addItem(spacerItem)
        self.ClearButton = QtGui.QPushButton(self.ButtonWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/services/service_new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClearButton.setIcon(icon)
        self.ClearButton.setObjectName("ClearButton")
        self.ButtonLayout.addWidget(self.ClearButton)
        self.AddUpdateButton = QtGui.QPushButton(self.ButtonWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/services/service_save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddUpdateButton.setIcon(icon1)
        self.AddUpdateButton.setObjectName("AddUpdateButton")
        self.ButtonLayout.addWidget(self.AddUpdateButton)
        self.DeleteButton = QtGui.QPushButton(self.ButtonWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/services/service_delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon2)
        self.DeleteButton.setObjectName("DeleteButton")
        self.ButtonLayout.addWidget(self.DeleteButton)
        self.AuthorLayout.addWidget(self.ButtonWidget)
        self.DialogLayout.addWidget(self.AuthorDetails)
        self.buttonBox = QtGui.QDialogButtonBox(AuthorsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.DialogLayout.addWidget(self.buttonBox)

        self.retranslateUi(AuthorsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AuthorsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AuthorsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AuthorsDialog)

    def retranslateUi(self, AuthorsDialog):
        AuthorsDialog.setWindowTitle(QtGui.QApplication.translate("AuthorsDialog", "Author Maintenance", None, QtGui.QApplication.UnicodeUTF8))
        self.AuthorDetails.setTitle(QtGui.QApplication.translate("AuthorsDialog", "Author Details", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "Display Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.FirstNameLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "First Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.LastNameLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "Last Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearButton.setToolTip(QtGui.QApplication.translate("AuthorsDialog", "Clear Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearButton.setText(QtGui.QApplication.translate("AuthorsDialog", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.AddUpdateButton.setToolTip(QtGui.QApplication.translate("AuthorsDialog", "Add Update Author", None, QtGui.QApplication.UnicodeUTF8))
        self.AddUpdateButton.setText(QtGui.QApplication.translate("AuthorsDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setToolTip(QtGui.QApplication.translate("AuthorsDialog", "Delete Author", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setText(QtGui.QApplication.translate("AuthorsDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBox.setToolTip(QtGui.QApplication.translate("AuthorsDialog", "Exit Screen", None, QtGui.QApplication.UnicodeUTF8))
