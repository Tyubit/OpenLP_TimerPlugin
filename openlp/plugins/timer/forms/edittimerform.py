import logging

from PySide6 import QtCore, QtWidgets, QtGui

from openlp.core.common.i18n import translate
from openlp.core.common.registry import Registry
from openlp.core.lib.ui import critical_error_message_box, find_and_set_in_combo_box

from openlp.plugins.timer.forms.edittimerdialog import Ui_TimerEditDialog
from openlp.plugins.timer.forms.edittimerslideform import EditTimerSlideForm
from openlp.plugins.timer.lib.db import TimerSlide

log = logging.getLogger(__name__)

class EditTimerForm(QtWidgets.QDialog, Ui_TimerEditDialog):
    """
    Class documentation goes here.
    """
    log.info('timer Editor loaded')

    def __init__(self, media_item, parent, manager):
        """
        Constructor
        """
        super(EditTimerForm, self).__init__(parent,
                                             QtCore.Qt.WindowType.WindowSystemMenuHint |
                                             QtCore.Qt.WindowType.WindowTitleHint |
                                             QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.manager = manager
        self.media_item = media_item
        self.setup_ui(self)
        # Create other objects and forms.
        self.edit_slide_form = EditTimerSlideForm(self)
        # Connecting signals and slots
        self.timer_checkbox.stateChanged.connect(self.timer_checkbox_state_changed)
        self.clocktimer_checkbox.stateChanged.connect(self.clocktimer_checkbox_state_changed)
    
    def load_themes(self, theme_list):
        """
        Load a list of themes into the themes combo box.

        :param theme_list: The list of themes to load.
        """
        self.theme_combo_box.clear()
        self.theme_combo_box.addItem('')
        self.theme_combo_box.addItems(theme_list)

    def load_timer(self, id, preview=False):
        """
        Called when editing or creating a new timer.

        :param id: The timer's id. If zero, then a new timer is created.
        :param preview: States whether the timer is edited while being previewed in the preview panel.
        """
        if id == 0:
            self.timer_slide = TimerSlide()
            self.title_edit.setText('')
        else:
            self.timer_slide = self.manager.get_object(TimerSlide, id)
            self.title_edit.setText(self.timer_slide.title)
            self.text_edit.setText(self.timer_slide.text)
        self.title_edit.setFocus()

    def timer_checkbox_state_changed(self, state):
        """
        Called when the timer checkbox is toggled.
        :param state: The new state of the checkbox.
        """
        if state == 2:
            self.timer_options.show()
        else:
            self.timer_options.hide()
    
    def clocktimer_checkbox_state_changed(self, state):
        """
        Called when the clocktimer checkbox is toggled.
        :param state: The new state of the checkbox.
        """
        if state == 2:
            self.clocktimer_options.show()
        else:
            self.clocktimer_options.hide()
    
