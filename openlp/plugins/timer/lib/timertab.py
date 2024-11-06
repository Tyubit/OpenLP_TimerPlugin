from PySide6 import QtCore, QtWidgets

from openlp.core.common.i18n import translate
from openlp.core.common.registry import Registry
from openlp.core.lib.settingstab import SettingsTab


class TimerTab(SettingsTab):
    print("TimerTab loaded")
    """
    TimerTab is the timer settings tab in the settings dialog.
    """
    def setup_ui(self):
        self.setObjectName('timerTab')
        super(TimerTab, self).setup_ui()
        self.timer_mode_group_box = QtWidgets.QGroupBox(self.left_column)
        self.timer_mode_group_box.setObjectName('timer_mode_group_box')
        self.timer_mode_layout = QtWidgets.QFormLayout(self.timer_mode_group_box)
        self.timer_mode_layout.setObjectName('timer_mode_layout')
        self.add_from_service_checkbox = QtWidgets.QCheckBox(self.timer_mode_group_box)
        self.add_from_service_checkbox.setObjectName('add_from_service_checkbox')
        self.timer_mode_layout.addRow(self.add_from_service_checkbox)
        self.left_layout.addWidget(self.timer_mode_group_box)
        self.left_layout.addStretch()
        self.right_layout.addStretch()
        self.add_from_service_checkbox.stateChanged.connect(self.on_add_from_service_check_box_changed)

    def retranslateUi(self):
        self.custom_mode_group_box.setTitle(translate('TimerPlugin.TimerTab', 'Timer Display'))
        self.add_from_service_checkbox.setText(translate('TimerPlugin.TimerTab',
                                               'Import missing timer slides from service files'))

    def on_add_from_service_check_box_changed(self, check_state):
        """
        Allows service items to create Timer items.

        :param check_state: The current check box state
        """
        self.update_load = (check_state == QtCore.Qt.CheckState.Checked)

    def load(self):
        """
        Load the settings into the dialog
        """
        self.update_load = self.settings.value('timer/add timer from service')
        self.add_from_service_checkbox.setChecked(self.update_load)

    def save(self):
        """
        Save the Dialog settings
        """
        self.settings.setValue('timer/add timer from service', self.update_load)
        if self.tab_visited:
            self.settings_form.register_post_process('timer_config_updated')
        self.tab_visited = False
