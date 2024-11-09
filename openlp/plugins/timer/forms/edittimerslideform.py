import logging

from PySide6 import QtCore, QtWidgets

from .edittimerslidedialog import Ui_TimerSlideEditDialog

log = logging.getLogger(__name__)

class EditTimerSlideForm(QtWidgets.QDialog, Ui_TimerSlideEditDialog):
    """
    Class documentation goes here.
    """
    log.info('Timer Slide Editor loaded')

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(EditTimerSlideForm, self).__init__(parent,
                                                  QtCore.Qt.WindowType.WindowSystemMenuHint |
                                                  QtCore.Qt.WindowType.WindowTitleHint |
                                                  QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui(self)