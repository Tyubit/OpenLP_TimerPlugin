# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auditdetaildialog.ui'
#
# Created: Sun Oct 11 11:40:02 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AuditDetailDialog(object):
    def setupUi(self, AuditDetailDialog):
        AuditDetailDialog.setObjectName("AuditDetailDialog")
        AuditDetailDialog.resize(593, 501)
        self.buttonBox = QtGui.QDialogButtonBox(AuditDetailDialog)
        self.buttonBox.setGeometry(QtCore.QRect(420, 470, 170, 25))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.FileGroupBox = QtGui.QGroupBox(AuditDetailDialog)
        self.FileGroupBox.setGeometry(QtCore.QRect(10, 370, 571, 70))
        self.FileGroupBox.setObjectName("FileGroupBox")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.FileGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.FileLineEdit = QtGui.QLineEdit(self.FileGroupBox)
        self.FileLineEdit.setObjectName("FileLineEdit")
        self.horizontalLayout.addWidget(self.FileLineEdit)
        self.SaveFilePushButton = QtGui.QPushButton(self.FileGroupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/exports/export_load.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveFilePushButton.setIcon(icon)
        self.SaveFilePushButton.setObjectName("SaveFilePushButton")
        self.horizontalLayout.addWidget(self.SaveFilePushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.layoutWidget = QtGui.QWidget(AuditDetailDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 561, 361))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ReportTypeGroup = QtGui.QGroupBox(self.layoutWidget)
        self.ReportTypeGroup.setObjectName("ReportTypeGroup")
        self.layoutWidget1 = QtGui.QWidget(self.ReportTypeGroup)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 40, 481, 23))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.ReportHorizontalLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.ReportHorizontalLayout.setObjectName("ReportHorizontalLayout")
        self.SummaryReport = QtGui.QRadioButton(self.layoutWidget1)
        self.SummaryReport.setObjectName("SummaryReport")
        self.ReportHorizontalLayout.addWidget(self.SummaryReport)
        self.DetailedReport = QtGui.QRadioButton(self.layoutWidget1)
        self.DetailedReport.setChecked(True)
        self.DetailedReport.setObjectName("DetailedReport")
        self.ReportHorizontalLayout.addWidget(self.DetailedReport)
        self.verticalLayout_3.addWidget(self.ReportTypeGroup)
        self.DateRangeGroupBox = QtGui.QGroupBox(self.layoutWidget)
        self.DateRangeGroupBox.setObjectName("DateRangeGroupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.DateRangeGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.DateHorizontalLayout = QtGui.QHBoxLayout()
        self.DateHorizontalLayout.setObjectName("DateHorizontalLayout")
        self.FromDateEdit = QtGui.QDateEdit(self.DateRangeGroupBox)
        self.FromDateEdit.setCalendarPopup(True)
        self.FromDateEdit.setObjectName("FromDateEdit")
        self.DateHorizontalLayout.addWidget(self.FromDateEdit)
        self.To = QtGui.QLabel(self.DateRangeGroupBox)
        self.To.setObjectName("To")
        self.DateHorizontalLayout.addWidget(self.To)
        self.ToDateEdit = QtGui.QDateEdit(self.DateRangeGroupBox)
        self.ToDateEdit.setCalendarPopup(True)
        self.ToDateEdit.setObjectName("ToDateEdit")
        self.DateHorizontalLayout.addWidget(self.ToDateEdit)
        self.verticalLayout_2.addLayout(self.DateHorizontalLayout)
        self.verticalLayout_3.addWidget(self.DateRangeGroupBox)
        self.TimePeriodGroupBox = QtGui.QGroupBox(self.layoutWidget)
        self.TimePeriodGroupBox.setObjectName("TimePeriodGroupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.TimePeriodGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.FirstHorizontalLayout = QtGui.QHBoxLayout()
        self.FirstHorizontalLayout.setObjectName("FirstHorizontalLayout")
        self.FirstCheckBox = QtGui.QCheckBox(self.TimePeriodGroupBox)
        self.FirstCheckBox.setChecked(True)
        self.FirstCheckBox.setObjectName("FirstCheckBox")
        self.FirstHorizontalLayout.addWidget(self.FirstCheckBox)
        self.FirstFromTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.FirstFromTimeEdit.setTime(QtCore.QTime(9, 0, 0))
        self.FirstFromTimeEdit.setObjectName("FirstFromTimeEdit")
        self.FirstHorizontalLayout.addWidget(self.FirstFromTimeEdit)
        self.FirstTo = QtGui.QLabel(self.TimePeriodGroupBox)
        self.FirstTo.setObjectName("FirstTo")
        self.FirstHorizontalLayout.addWidget(self.FirstTo)
        self.FirstToTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.FirstToTimeEdit.setCalendarPopup(True)
        self.FirstToTimeEdit.setTime(QtCore.QTime(10, 0, 0))
        self.FirstToTimeEdit.setObjectName("FirstToTimeEdit")
        self.FirstHorizontalLayout.addWidget(self.FirstToTimeEdit)
        self.verticalLayout.addLayout(self.FirstHorizontalLayout)
        self.SecondHorizontalLayout = QtGui.QHBoxLayout()
        self.SecondHorizontalLayout.setObjectName("SecondHorizontalLayout")
        self.SecondCheckBox = QtGui.QCheckBox(self.TimePeriodGroupBox)
        self.SecondCheckBox.setChecked(True)
        self.SecondCheckBox.setObjectName("SecondCheckBox")
        self.SecondHorizontalLayout.addWidget(self.SecondCheckBox)
        self.SecondFromTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.SecondFromTimeEdit.setTime(QtCore.QTime(10, 45, 0))
        self.SecondFromTimeEdit.setObjectName("SecondFromTimeEdit")
        self.SecondHorizontalLayout.addWidget(self.SecondFromTimeEdit)
        self.SecondTo = QtGui.QLabel(self.TimePeriodGroupBox)
        self.SecondTo.setObjectName("SecondTo")
        self.SecondHorizontalLayout.addWidget(self.SecondTo)
        self.SecondToTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.SecondToTimeEdit.setObjectName("SecondToTimeEdit")
        self.SecondHorizontalLayout.addWidget(self.SecondToTimeEdit)
        self.verticalLayout.addLayout(self.SecondHorizontalLayout)
        self.ThirdHorizontalLayout = QtGui.QHBoxLayout()
        self.ThirdHorizontalLayout.setObjectName("ThirdHorizontalLayout")
        self.ThirdCheckBox = QtGui.QCheckBox(self.TimePeriodGroupBox)
        self.ThirdCheckBox.setChecked(True)
        self.ThirdCheckBox.setObjectName("ThirdCheckBox")
        self.ThirdHorizontalLayout.addWidget(self.ThirdCheckBox)
        self.ThirdFromTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.ThirdFromTimeEdit.setTime(QtCore.QTime(18, 30, 0))
        self.ThirdFromTimeEdit.setObjectName("ThirdFromTimeEdit")
        self.ThirdHorizontalLayout.addWidget(self.ThirdFromTimeEdit)
        self.ThirdTo = QtGui.QLabel(self.TimePeriodGroupBox)
        self.ThirdTo.setObjectName("ThirdTo")
        self.ThirdHorizontalLayout.addWidget(self.ThirdTo)
        self.ThirdToTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.ThirdToTimeEdit.setTime(QtCore.QTime(19, 30, 0))
        self.ThirdToTimeEdit.setObjectName("ThirdToTimeEdit")
        self.ThirdHorizontalLayout.addWidget(self.ThirdToTimeEdit)
        self.verticalLayout.addLayout(self.ThirdHorizontalLayout)
        self.verticalLayout_3.addWidget(self.TimePeriodGroupBox)

        self.retranslateUi(AuditDetailDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AuditDetailDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AuditDetailDialog.close)
        QtCore.QObject.connect(self.FirstCheckBox, QtCore.SIGNAL("stateChanged(int)"), AuditDetailDialog.changeFirstService)
        QtCore.QObject.connect(self.SecondCheckBox, QtCore.SIGNAL("stateChanged(int)"), AuditDetailDialog.changeSecondService)
        QtCore.QObject.connect(self.ThirdCheckBox, QtCore.SIGNAL("stateChanged(int)"), AuditDetailDialog.changeThirdService)
        QtCore.QObject.connect(self.SaveFilePushButton, QtCore.SIGNAL("pressed()"), AuditDetailDialog.defineOutputLocation)
        QtCore.QMetaObject.connectSlotsByName(AuditDetailDialog)

    def retranslateUi(self, AuditDetailDialog):
        AuditDetailDialog.setWindowTitle(QtGui.QApplication.translate("AuditDetailDialog", "Audit Detail Extraction", None, QtGui.QApplication.UnicodeUTF8))
        self.FileGroupBox.setTitle(QtGui.QApplication.translate("AuditDetailDialog", "Report Location", None, QtGui.QApplication.UnicodeUTF8))
        self.ReportTypeGroup.setTitle(QtGui.QApplication.translate("AuditDetailDialog", "Report Type", None, QtGui.QApplication.UnicodeUTF8))
        self.SummaryReport.setText(QtGui.QApplication.translate("AuditDetailDialog", "Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.DetailedReport.setText(QtGui.QApplication.translate("AuditDetailDialog", "Detailed", None, QtGui.QApplication.UnicodeUTF8))
        self.DateRangeGroupBox.setTitle(QtGui.QApplication.translate("AuditDetailDialog", "Select Date Range", None, QtGui.QApplication.UnicodeUTF8))
        self.FromDateEdit.setDisplayFormat(QtGui.QApplication.translate("AuditDetailDialog", "dd/MM/yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.To.setText(QtGui.QApplication.translate("AuditDetailDialog", "to", None, QtGui.QApplication.UnicodeUTF8))
        self.ToDateEdit.setDisplayFormat(QtGui.QApplication.translate("AuditDetailDialog", "dd/MM/yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.TimePeriodGroupBox.setTitle(QtGui.QApplication.translate("AuditDetailDialog", "Select Time Periods", None, QtGui.QApplication.UnicodeUTF8))
        self.FirstCheckBox.setText(QtGui.QApplication.translate("AuditDetailDialog", "First Service", None, QtGui.QApplication.UnicodeUTF8))
        self.FirstFromTimeEdit.setDisplayFormat(QtGui.QApplication.translate("AuditDetailDialog", "hh:mm AP", None, QtGui.QApplication.UnicodeUTF8))
        self.FirstTo.setText(QtGui.QApplication.translate("AuditDetailDialog", "to", None, QtGui.QApplication.UnicodeUTF8))
        self.FirstToTimeEdit.setDisplayFormat(QtGui.QApplication.translate("AuditDetailDialog", "hh:mm AP", None, QtGui.QApplication.UnicodeUTF8))
        self.SecondCheckBox.setText(QtGui.QApplication.translate("AuditDetailDialog", "Second Service", None, QtGui.QApplication.UnicodeUTF8))
        self.SecondFromTimeEdit.setDisplayFormat(QtGui.QApplication.translate("AuditDetailDialog", "hh:mm AP", None, QtGui.QApplication.UnicodeUTF8))
        self.SecondTo.setText(QtGui.QApplication.translate("AuditDetailDialog", "to", None, QtGui.QApplication.UnicodeUTF8))
        self.SecondToTimeEdit.setDisplayFormat(QtGui.QApplication.translate("AuditDetailDialog", "hh:mm AP", None, QtGui.QApplication.UnicodeUTF8))
        self.ThirdCheckBox.setText(QtGui.QApplication.translate("AuditDetailDialog", "Third Service", None, QtGui.QApplication.UnicodeUTF8))
        self.ThirdFromTimeEdit.setDisplayFormat(QtGui.QApplication.translate("AuditDetailDialog", "hh:mm AP", None, QtGui.QApplication.UnicodeUTF8))
        self.ThirdTo.setText(QtGui.QApplication.translate("AuditDetailDialog", "to", None, QtGui.QApplication.UnicodeUTF8))
        self.ThirdToTimeEdit.setDisplayFormat(QtGui.QApplication.translate("AuditDetailDialog", "hh:mm AP", None, QtGui.QApplication.UnicodeUTF8))
