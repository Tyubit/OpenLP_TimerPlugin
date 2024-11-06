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
        self.setObjectName('CustomTab')
        super(TimerTab, self).setup_ui()

    def retranslateUi(self):
        pass   

    def load(self):
        pass

    def save(self):
        pass
    
    def initialise(self):
        pass
