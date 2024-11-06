import logging
from openlp.core.common.settings import Settings
from openlp.core.common.i18n import translate
from openlp.core.lib import build_icon
from openlp.core.common.registry import Registry
from openlp.core.db.manager import DBManager
from openlp.core.lib.plugin import Plugin, StringContent
from openlp.core.state import State
from openlp.core.ui.icons import UiIcons
from openlp.core.common.enum import PluginStatus

from openlp.plugins.timer.lib.mediaitem import TimerMediaItem
from openlp.plugins.timer.lib.timertab import TimerTab
from openlp.plugins.timer.lib.db import init_schema

from PySide6 import QtCore, QtGui

log = logging.getLogger(__name__)

__default_settings__ = {
    'timer/db type': 'sqlite',
    'timer/status': PluginStatus.Inactive,
    'timer/db username': '',
    'timer/db password': '',
    'timer/db hostname': '',
    'timer/db database': '',
    'timer/theme': None,
    'timer/last directory': None,
    'shortcuts/listViewTimerDeleteItem': [QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Delete)],
    'shortcuts/listViewTimerPreviewItem': [QtGui.QKeySequence(QtCore.Qt.Key.Key_Return),
                                            QtGui.QKeySequence(QtCore.Qt.Key.Key_Enter)],
    'shortcuts/listViewTimerLiveItem': [QtGui.QKeySequence(QtCore.Qt.Key.Key_Shift + QtCore.Qt.Key.Key_Return),
                                            QtGui.QKeySequence(QtCore.Qt.Key.Key_Shift + QtCore.Qt.Key.Key_Enter)],
    'shortcuts/listViewTimerServiceItem': [QtGui.QKeySequence(QtCore.Qt.Key.Key_Plus),
                                            QtGui.QKeySequence(QtCore.Qt.Key.Key_Equal)],
}

class TimerPlugin(Plugin):
    log.info('Timer Plugin loaded')
    print("Timer Plugin initialized:")
    
    def __init__(self):
        """
        add plugin settings to the registry
        """
        Settings().extend_default_settings(__default_settings__)

        super(TimerPlugin, self).__init__('timer',__default_settings__, TimerMediaItem, TimerTab)
        self.weight = -11
        self.db_manager = DBManager(self.name, init_schema)
        self.icon_path = UiIcons().custom
        Registry().register('timer_manager',self.db_manager)
        self.icon = build_icon(self.icon_path)
        State().add_service(self.name, self.weight, is_plugin=True)
        State().update_pre_conditions(self.name, self.check_pre_conditions())

    @staticmethod
    def about():
        about_text = translate('TimerPlugin', '<strong>Timer Slide Plugin</strong><br />The timer slide plugin '
                                'provides the ability to display a live countdown, timer to a display device.')
        return about_text

    def check_pre_conditions(self):
        """
        Check the plugin can run.
        """
        return self.db_manager.session is not None

    def set_plugin_text_strings(self):
        """
        Called to define all translatable texts of the plugin
        """
        # Name PluginList
        self.text_strings[StringContent.Name] = {
            'singular': translate('TimerPlugin', 'Timer Slide', 'name singular'),
            'plural': translate('TimerPlugin', 'Timer Slides', 'name plural')
        }
        # Name for MediaDockManager, SettingsManager
        self.text_strings[StringContent.VisibleName] = {
            'title': translate('TimerPlugin', 'Timer Slides', 'container title')
        }

        # Middle Header Bar
        tooltips = {
            'load': translate('TimerPlugin', 'Load a new timer slide.'),
            'import': translate('TimerPlugin', 'Import a timer slide.'),
            'new': translate('TimerPlugin', 'Add a new timer slide.'),
            'edit': translate('TimerPlugin', 'Edit the selected timer slide.'),
            'delete': translate('TimerPlugin', 'Delete the selected timer slide.'),
            'preview': translate('TimerPlugin', 'Preview the selected timer slide.'),
            'live': translate('TimerPlugin', 'Send the selected timer slide live.'),
            'service': translate('TimerPlugin', 'Add the selected timer slide to the service.')
        }
        self.set_plugin_ui_text_strings(tooltips)

    def uses_theme(self, theme):
        """
        Called to find out if the timer plugin is currently using a theme.

        Returns count of the times the theme is used.
        :param theme: Theme to be queried
        """
        return len(self.db_manager.get_all_objects(TimerSlide, TimerSlide.theme_name == theme))

    def rename_theme(self, old_theme, new_theme):
        """
        Renames a theme the timer plugin is using making the plugin use the new name.

        :param old_theme: The name of the theme the plugin should stop using.
        :param new_theme: The new name the plugin should now use.
        """
        timer_using_theme = self.db_manager.get_all_objects(TimerSlide, TimerSlide.theme_name == old_theme)
        for timer in timer_using_theme:
            timer.theme_name = new_theme
            self.db_manager.save_object(timer)

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info('Timer Finalising')
        # call timer manager to delete pco slides
        pco_slides = self.db_manager.get_all_objects(TimerSlide, TimerSlide.credits == 'pco')
        for slide in pco_slides:
            self.db_manager.delete_object(TimerSlide, slide.id)
        self.db_manager.finalise()
        Plugin.finalise(self)