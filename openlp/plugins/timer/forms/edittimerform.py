import logging

from PySide6 import QtCore, QtWidgets, QtGui
from datetime import datetime

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
        self.save_button.clicked.connect(self.on_save_button_clicked)
    
    def load_timer(self, id, preview=False):
        """
        Called when editing or creating a new timer.

        :param id: The timer's id. If zero, then a new timer is created.
        :param preview: States whether the timer is edited while being previewed in the preview panel.
        """
        current_time = datetime.now().time() 
        if id == 0:
            self.timer_slide = TimerSlide()
            self.title_edit.setText('')
            self.text_edit.setText('')
            self.timer_checkbox.setCheckState(QtCore.Qt.Checked)
            self.clocktimer_checkbox.setCheckState(QtCore.Qt.Unchecked)
            self.timer_hours_input.setText('0')
            self.timer_minutes_input.setText('0')
            self.clocktimer_options.setTime(QtCore.QTime(12, 30))
        else:
            self.timer_slide = self.manager.get_object(TimerSlide, id)
            print('db duration', self.timer_slide.timer_duration)
            self.title_edit.setText(self.timer_slide.title)
            self.text_edit.setText(self.timer_slide.text)
            self.timer_checkbox.setCheckState(QtCore.Qt.Checked if self.timer_slide.timer_use_timer else QtCore.Qt.Unchecked)
            self.clocktimer_checkbox.setCheckState(QtCore.Qt.Checked if self.timer_slide.timer_use_specific_time else QtCore.Qt.Unchecked)
            self.timer_hours_input.setText(str(self.timer_slide.timer_duration // 60))
            self.timer_minutes_input.setText(str(self.timer_slide.timer_duration % 60))
            self.clocktimer_options.setTime(QtCore.QTime((current_time.hour + (self.timer_slide.timer_duration // 60)-24), current_time.minute + (self.timer_slide.timer_duration % 60)))
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
    
    def accept(self):
        """
        Override the QDialog method to check if the timer slide has been saved before closing the dialog.
        """
        log.debug('accept')
        if self.save_timer():
            QtWidgets.QDialog.accept(self)
    
    def save_timer(self):
        """
        Saves the timer to the database.
        """
        current_time = datetime.now().time() 
        print('timer_duration',int(self.timer_hours_input.text())*60 + int(self.timer_minutes_input.text()))
        if not self._validate():
            print('not valid')
            return False
        self.timer_slide.title = self.title_edit.text()
        print("save", self.timer_slide.title)
        self.timer_slide.text = self.text_edit.text()
        self.timer_slide.timer_use_timer = self.timer_checkbox.checkState() == 2
        self.timer_slide.timer_use_specific_time = self.clocktimer_checkbox.checkState() == 2
        if (self.timer_checkbox.checkState() == QtCore.Qt.Checked):
            self.timer_slide.timer_duration = (int(self.timer_hours_input.text())*60 + int(self.timer_minutes_input.text()))
        else:
            time_left = (self.clocktimer_options.time().hour() - current_time.hour) * 60 + (self.clocktimer_options.time().minute() - current_time.minute)
            self.timer_slide.timer_duration = time_left if time_left > 0 else 24 * 60 + time_left
        success = self.manager.save_object(self.timer_slide)
        self.media_item.auto_select_id = self.timer_slide.id
        Registry().execute('timer_changed', self.timer_slide.id)
        return success
    
    def _validate(self):
        """
        Validates the user input.
        """
        if not self.title_edit.displayText():
            self.title_edit.setFocus()
            critical_error_message_box(translate('openlp.plugins.timer', 'Please enter a title.'))
            return False
        return True
    
    def on_save_button_clicked(self):
        """
        Called when the user clicks the save button.
        """
        log.debug('Timer save button clicked')
        print(self.timer_slide.id)
        if self.save_timer():
            Registry().execute('timer.save_timer')
    
    def provide_help(self):
        """
        Provide help within the form by opening the appropriate page of the openlp manual in the user's browser
        """