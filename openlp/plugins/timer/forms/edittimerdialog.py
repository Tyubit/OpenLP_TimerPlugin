from PySide6 import QtWidgets, QtGui, QtCore

from openlp.core.common.i18n import UiStrings, translate
from openlp.core.lib.ui import create_button, create_button_box
from openlp.core.ui.icons import UiIcons


class Ui_TimerEditDialog(object):
    def setup_ui(self, timer_edit_dialog):
        """
        Build the Edit Dialog UI
        :param timer_edit_dialog: The Dialog
        """
        # Set the dialog properties
        timer_edit_dialog.setObjectName('timer_edit_dialog')
        timer_edit_dialog.setWindowIcon(UiIcons().main_icon)
        timer_edit_dialog.resize(450, 150)
        self.dialog_layout = QtWidgets.QVBoxLayout(timer_edit_dialog)
        self.dialog_layout.setObjectName('dialog_layout')
        #Title Layout
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.setObjectName('title_layout')
        self.title_label = QtWidgets.QLabel(timer_edit_dialog)
        self.title_label.setObjectName('title_label')
        self.title_layout.addWidget(self.title_label)
        self.title_edit = QtWidgets.QLineEdit(timer_edit_dialog)
        self.title_label.setBuddy(self.title_edit)
        self.title_edit.setObjectName('title_edit')
        self.title_layout.addWidget(self.title_edit)
        self.dialog_layout.addLayout(self.title_layout)
        #Text Layout
        self.text_layout = QtWidgets.QHBoxLayout()
        self.text_layout.setObjectName('text_layout')
        self.text_label = QtWidgets.QLabel(timer_edit_dialog)
        self.text_label.setObjectName('text_label')
        self.text_layout.addWidget(self.text_label)
        self.text_edit = QtWidgets.QLineEdit(timer_edit_dialog)
        self.text_edit.setObjectName('text_edit')
        self.text_label.setBuddy(self.text_edit)
        self.text_layout.addWidget(self.text_edit)
        self.dialog_layout.addLayout(self.text_layout)
        #Checkbox Layout
        self.checkbox_layout = QtWidgets.QHBoxLayout()
        self.checkbox_layout.setObjectName('checkbox_layout')
        #Checkbox dropdown Layout
        self.dropdown_layout = QtWidgets.QHBoxLayout()
        self.dropdown_layout.setObjectName('dropdown_layout')
        #Timer Checkbox Layout
        self.timer_checkbox = QtWidgets.QCheckBox("Timer", timer_edit_dialog)
        self.timer_checkbox.setObjectName('timer_checkbox')
        self.timer_checkbox.setChecked(True)
        self.checkbox_layout.addWidget(self.timer_checkbox)
        #Timer Checkbox dropdown
        self.timer_options = QtWidgets.QWidget()
        self.timer_options_layout = QtWidgets.QHBoxLayout(self.timer_options)
        self.timer_hours_label = QtWidgets.QLabel("Hours:")
        self.timer_hours_input = QtWidgets.QLineEdit()
        self.timer_hours_input.setValidator(QtGui.QIntValidator(0, 999))
        self.timer_options_layout.addWidget(self.timer_hours_label)
        self.timer_options_layout.addWidget(self.timer_hours_input)
        self.timer_minutes_label = QtWidgets.QLabel("Minutes:")
        self.timer_minutes_input = QtWidgets.QLineEdit()
        self.timer_minutes_input.setValidator(QtGui.QIntValidator(0, 999))
        self.timer_options_layout.addWidget(self.timer_minutes_label)
        self.timer_options_layout.addWidget(self.timer_minutes_input)
        self.dropdown_layout.addWidget(self.timer_options)
        self.timer_options.show()
        #Specific Timer Layout
        self.clocktimer_checkbox = QtWidgets.QCheckBox("Clock Timer", timer_edit_dialog)
        self.clocktimer_checkbox.setObjectName('clocktimer_checkbox')
        self.checkbox_layout.addWidget(self.clocktimer_checkbox)
        self.checkbox_group = QtWidgets.QButtonGroup()
        self.checkbox_group.setExclusive(True)  # Set exclusivity
        self.checkbox_group.addButton(self.timer_checkbox)
        self.checkbox_group.addButton(self.clocktimer_checkbox)
        #Specific Timer dropdown
        self.clocktimer_options = QtWidgets.QTimeEdit(timer_edit_dialog)
        self.clocktimer_options.setObjectName('clocktimer_options')
        self.clocktimer_options.setDisplayFormat("HH:mm")
        self.clocktimer_options.setTime(QtCore.QTime(12, 30))
        self.dropdown_layout.addWidget(self.clocktimer_options)
        self.clocktimer_options.hide()
        self.dialog_layout.addLayout(self.checkbox_layout)
        self.dialog_layout.addLayout(self.dropdown_layout)
        #Bottom Form Layout
        self.bottom_form_layout = QtWidgets.QFormLayout()
        self.bottom_form_layout.setObjectName('bottom_form_layout')
        self.dialog_layout.addLayout(self.bottom_form_layout)
        self.button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.setObjectName('button_layout')
        self.button_box = create_button_box(timer_edit_dialog, 'button_box', ['cancel', 'save', 'help'])
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.dialog_layout.addWidget(self.button_box)
    
        self.retranslate_ui(timer_edit_dialog)
    
    def retranslate_ui(self, timer_edit_dialog):
        timer_edit_dialog.setWindowTitle(translate('TimerPlugin.EditTimerForm', 'Edit Timer'))
        self.title_label.setText(translate('TimerPlugin.EditTimerForm', '&Title:'))
        self.text_label.setText(translate('TimerPlugin.EditTimerForm', '&Text(optional):'))
        self.save_button.setText(UiStrings().SaveAndClose)