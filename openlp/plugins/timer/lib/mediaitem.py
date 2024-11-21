import logging
from typing import Any

from PySide6 import QtCore, QtWidgets
from sqlalchemy.sql import and_, func, or_

from openlp.core.common.i18n import UiStrings, translate
from openlp.core.common.registry import Registry
from openlp.core.lib import check_item_selected
from openlp.core.lib.mediamanageritem import MediaManagerItem
from openlp.core.lib.plugin import PluginStatus
from openlp.core.lib.serviceitem import ItemCapabilities
from openlp.core.lib import ServiceItemContext, check_item_selected
from openlp.core.lib.ui import create_widget_action
from openlp.core.ui.icons import UiIcons

from openlp.plugins.timer.lib.db import TimerSlide
from openlp.plugins.timer.forms.edittimerform import EditTimerForm

log = logging.getLogger(__name__)

class TimerSearch(object):
    """
    An enumeration for timer search methods.
    """
    Titles = 1
class TimerMediaItem(MediaManagerItem):
    """
    This is the timer media manager item for timers.
    """
    log.info('Timer Media Item loaded')
    print("TimerMediaItem loaded")

    timer_add_to_service = QtCore.Signal(list)
    def __init__(self, parent, plugin):
        self.icon_path = 'timer/timer'
        super(TimerMediaItem, self).__init__(parent, plugin)

    def setup_item(self):
        """
        Do some additional setup.
        """
        self.edit_timer_form = EditTimerForm(self, self.main_window, self.plugin.db_manager)
        self.single_service_item = True
        self.quick_preview_allowed = True
        self.has_search = True
        self.remote_timer = -1
    
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
        """
        Add the Timer Context Actions
        """
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
        if search_type == TimerSearch.Titles:
            log.debug('Titles Search')
            search_results = self.plugin.db_manager.get_all_objects(TimerSlide,
                                                                            TimerSlide.title.like(search_keywords),
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
                                       timer_duration = old_timer_slide.timer_duration,
                                       timer_use_timer = old_timer_slide.timer_use_timer,
                                       timer_use_specific_time = old_timer_slide.timer_use_specific_time)
        self.plugin.db_manager.save_object(new_timer_slide)
        Registry().execute('timer_changed', new_timer_slide.id)
        self.on_search_text_button_clicked()

    def on_new_click(self):
        """
        Handle the New item event
        """
        self.edit_timer_form.load_timer(0)
        self.edit_timer_form.exec()
        self.on_clear_text_button_click()
        self.on_selection_change()
    
    def on_edit_click(self):
        """
        Edit a timer item
        """
        if check_item_selected(self.list_view, UiStrings().SelectEdit):
            item = self.list_view.currentItem()
            item_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
            self.edit_timer_form.load_timer(item_id,False)
            self.edit_timer_form.exec()
            self.auto_select_id = -1
            self.on_search_text_button_clicked()
    
    def on_delete_click(self):
        """
        Remove a timer item from the list and database
        """
        if(check_item_selected(self.list_view, UiStrings().SelectDelete)):
            item = self.list_view.currentItem()
            if QtWidgets.QMessageBox.question(
                    self, UiStrings().ConfirmDelete,
                    translate('OpenLP.MediaManagerItem', 'Are you sure you want to delete this item?').format(item),
                    defaultButton=QtWidgets.QMessageBox.StandardButton.Yes) == QtWidgets.QMessageBox.StandardButton.No:
                return
            row_list = [item.row() for item in self.list_view.selectedIndexes()]
            row_list.sort(reverse=True)
            id_list = [item.data(QtCore.Qt.ItemDataRole.UserRole) for item in self.list_view.selectedIndexes()]
            for id in id_list:
                self.plugin.db_manager.delete_object(TimerSlide, id)
                Registry().execute('timer_deleted', id)
            self.on_search_text_button_clicked()
    
    def on_focus(self):
        """
        Set the focus
        """
        self.search_text_edit.setFocus()
        self.search_text_edit.selectAll()
    
    def config_update(self):
        """
        Config has been updated so reload values
        """
        log.debug('Config loaded')
        self.is_search_as_you_type_enabled = self.settings.value('advanced/search as type')
    
    def retranslate_ui(self):
        """
        Translate the UI
        """
        self.search_text_label.setText('{text}:'.format(text=UiStrings().Search))
        self.search_text_button.setText(UiStrings().Search)
    
    def initialise(self):
        """
        Initialise the UI so it can provide Searches
        """
        self.search_text_edit.set_search_types([(TimerSearch.Titles, UiIcons().search, translate('SongsPlugin.MediaItem', 'Titles'),
                                                 translate('SongsPlugin.MediaItem', 'Search Titles...'))])
        self.load_list(self.plugin.db_manager.get_all_objects(TimerSlide, order_by_ref=TimerSlide.title))
        self.config_update()
    
    def load_list(self,timer_slides = None, target_group = None):
        """
        Load the list of Timer items
        :param timer_slides: The list of Timer items
        :param target_group: The group to add the Timer items to
        """
        print(f"Loaded timer slides: {timer_slides}")
        self.save_auto_select_id()
        self.list_view.clear()  
        if not timer_slides:
            timer_slides = self.plugin.db_manager.get_all_objects(TimerSlide, order_by_ref=TimerSlide.title)
        timer_slides.sort()
        for timer_slide in timer_slides:
            timer_name = QtWidgets.QListWidgetItem(timer_slide.title)
            timer_name.setData(QtCore.Qt.ItemDataRole.UserRole, timer_slide.id)
            self.list_view.addItem(timer_name)
            #Auto-select the timer
            if timer_slide.id == self.auto_select_id:
                self.list_view.setCurrentItem(timer_name)
        self.auto_select_id = -1
    
    @QtCore.Slot(str, bool, result=list)
    def search(self, string: str, show_error: bool = True) -> list[list[Any]]:
        """
        Search the database for a given item.

        :param string: The search string
        :param show_error: The error string to be show.
        """
        search = '%{search}%'.format(search=string.lower())
        search_results = self.plugin.db_manager.get_all_objects(TimerSlide,
                                                                or_(func.lower(TimerSlide.title).like(search),
                                                                    func.lower(TimerSlide.title).like(search)),
                                                                order_by_ref=TimerSlide.title)
        return [[timer.id, timer.title] for timer in search_results]
    
    def generate_slide_data(self, service_item, *, item=None, **kwargs):
        """
        Generate the slide data. Needs to be implemented by the plugin.
        :param service_item: To be updated
        :param item: The timer database item to be used
        :param kwargs: Consume other unused args specified by the base implementation, but not use by this one.
        """
        item_id = self._get_id_of_item_to_generate(item, self.remote_timer)
        service_item.add_capability(ItemCapabilities.CanEdit)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.OnLoadUpdate)
        service_item.add_capability(ItemCapabilities.CanSoftBreak)
        service_item.add_capability(ItemCapabilities.CanAutoStartForLive)
        s
        timer_slide = self.plugin.db_manager.get_object(TimerSlide, item_id)
        title = timer_slide.title
        text = timer_slide.text
        print(timer_slide)
        timer_duration = str(timer_slide.timer_duration)
        theme = timer_slide.theme_name
        service_item.edit_id = item_id
        if theme:
            service_item.theme = theme
        service_item.title = title
        service_item.processor = 'qt6'
        service_item.add_from_command(filename, name, self.clapperboard)
        service_item.add_from_text(f"{text}, {int(timer_duration)}")
        return True
    
    def service_load(self, item):
        """
        Triggered by a timer item being loaded by the service manager.

        :param item: The service Item from the service to load found in the database.
        """
        log.debug('service_load')
        print('service_load')

        if self.plugin.status != PluginStatus.Active:
            return
        self.plugin.service_manager.update_service_item(item)





