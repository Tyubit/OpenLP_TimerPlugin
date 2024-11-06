import logging
from typing import Any

from PySide6 import QtCore, QtWidgets
from sqlalchemy.sql import and_, func, or_

from openlp.core.common.enum import CustomSearch
from openlp.core.common.i18n import UiStrings, translate
from openlp.core.common.registry import Registry
from openlp.core.lib import check_item_selected
from openlp.core.lib.mediamanageritem import MediaManagerItem
from openlp.core.lib.plugin import PluginStatus
from openlp.core.lib.serviceitem import ItemCapabilities
from openlp.core.lib.ui import create_widget_action
from openlp.core.ui.icons import UiIcons

from openlp.plugins.timer.lib.db import TimerSlide

log = logging.getLogger(__name__)

class TimerMediaItem(MediaManagerItem):
    """
    This is the timer media manager item for timers.
    """
    log.info('Timer Media Item loaded')
    print("TimerMediaItem loaded")

    def __init__(self, parent, plugin):
        self.icon_path = 'timer/timer'
        super(TimerMediaItem, self).__init__(parent, plugin)

    def setup_item(self):
        """
        Do some additional setup.
        """
        self.single_service_item = False
        self.quick_preview_allowed = True
        self.has_search = True


    def add_end_header_bar(self):
        """
        Add the Timer End Head bar and register events and functions
        """
        self.toolbar.addSeparator()
        self.add_search_to_toolbar()
        # Signals and slots
        self.search_text_edit.cleared.connect(self.on_clear_text_button_click)
        self.search_text_edit.searchTypeChanged.connect(self.on_search_text_button_clicked)
        Registry().register_function('timer_load_list', self.load_list)
        Registry().register_function('timer_preview', self.on_preview_click)
    
    def add_custom_context_actions(self):
        create_widget_action(self.list_view, separator=True)
        create_widget_action(
            self.list_view, text=translate('OpenLP.MediaManagerItem', '&Clone'), icon=UiIcons().clone,
            triggers=self.on_clone_click)
    
    def on_clear_text_button_click(self):
        """
        Clear the search text.
        """
        self.search_text_edit.clear()
        self.on_search_text_button_clicked()

    def on_search_text_button_clicked(self):
        """
        Search the plugin database
        """
        # Reload the list considering the new search type.
        search_type = self.search_text_edit.current_search_type()
        search_keywords = '%{search}%'.format(search=self.whitespace.sub(' ', self.search_text_edit.displayText()))
        if search_type == CustomSearch.Titles:
            log.debug('Titles Search')
            search_results = self.plugin.db_manager.get_all_objects(TimerSlide,
                                                                            TimerSlide.title.like(search_keywords),
                                                                            order_by_ref=TimerSlide.title)
            self.load_list(search_results)
        elif search_type == CustomSearch.Themes:
            log.debug('Theme Search')
            search_results = self.plugin.db_manager.get_all_objects(TimerSlide,
                                                                            TimerSlide.theme_name.like(search_keywords),
                                                                            order_by_ref=TimerSlide.title)
            self.load_list(search_results)
    
    def on_search_text_edit_changed(self, text):
        """
        If search as type enabled invoke the search on each key press. If the Title is being searched do not start until
        2 characters have been entered.

        :param text: The search text
        """
        if self.is_search_as_you_type_enabled:
            search_length = 2
            if len(text) > search_length:
                self.on_search_text_button_clicked()
            elif not text:
                self.on_clear_text_button_click()
    
    def on_clone_click(self):
        """
        Clone the selected Timer item
        """
        item = self.list_view.currentItem()
        item_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
        old_timer_slide = self.plugin.db_manager.get_object(TimerSlide, item_id)
        new_timer_slide = TimerSlide(title='{title} <{text}>'.format(title=old_timer_slide.title,
                                                                       text=translate('TimerSlide.MediaItem',
                                                                                      'copy', 'For item cloning')),
                                       text=old_timer_slide.text,
                                       credits=old_timer_slide.credits,
                                       theme_name=old_timer_slide.theme_name)
        self.plugin.db_manager.save_object(new_timer_slide)
        Registry().execute('timer_changed', new_timer_slide.id)
        self.on_search_text_button_clicked()

    
    
    




