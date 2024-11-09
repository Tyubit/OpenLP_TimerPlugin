from PySide6 import QtWidgets

from openlp.core.common.i18n import UiStrings, translate
from openlp.core.lib.ui import create_button, create_button_box
from openlp.core.ui.icons import UiIcons
from openlp.core.widgets.edits import SpellTextEdit


class Ui_TimerSlideEditDialog(object):
    def setup_ui(self, timer_slide_edit_dialog):
        timer_slide_edit_dialog.setObjectName('timer_slide_edit_dialog')
        timer_slide_edit_dialog.setWindowIcon(UiIcons().main_icon)
        timer_slide_edit_dialog.resize(350, 300)
        self.dialog_layout = QtWidgets.QVBoxLayout(timer_slide_edit_dialog)