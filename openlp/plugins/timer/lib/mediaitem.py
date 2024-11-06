import logging
from pathlib import Path
from typing import Any

from PySide6 import QtCore, QtWidgets

from openlp.core.common.applocation import AppLocation
from openlp.core.common.i18n import UiStrings, translate
from openlp.core.common.registry import Registry
from openlp.core.lib import ServiceItemContext, build_icon, check_item_selected
from openlp.core.lib.mediamanageritem import MediaManagerItem
from openlp.core.lib.serviceitem import ItemCapabilities
from openlp.core.lib.ui import create_widget_action, critical_error_message_box
from openlp.core.ui.icons import UiIcons

from openlp.plugins.timer.lib.db import TimerSlide

log = logging.getLogger(__name__)

class TimerMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for timers.
    """
    log.info('Timer Media Item loaded')
    print("TimerMediaItem loaded")

    def __init__(self, parent, plugin):
        self.icon_path = 'images/image'
        super(TimerMediaItem, self).__init__(parent, plugin)

    def setup_item(self):
        """
        Do some additional setup.
        """
        self.single_service_item = False
        self.quick_preview_allowed = True
        self.has_search = True

