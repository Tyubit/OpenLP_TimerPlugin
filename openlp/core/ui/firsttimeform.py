# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2019 OpenLP Developers                                   #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
This module contains the first time wizard.
"""
import json
import logging
import time
import urllib.error
import urllib.parse
import urllib.request
from tempfile import gettempdir

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import clean_button_text, trace_error_handler
from openlp.core.common.applocation import AppLocation
from openlp.core.common.httputils import DownloadWorker, download_file, get_url_file_size, get_web_page
from openlp.core.common.i18n import translate
from openlp.core.common.mixins import RegistryProperties
from openlp.core.common.path import Path, create_paths
from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.core.lib import build_icon
from openlp.core.lib.plugin import PluginStatus
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.threading import get_thread_worker, is_thread_finished, run_thread
from openlp.core.ui.firsttimewizard import FirstTimePage, UiFirstTimeWizard
from openlp.core.ui.icons import UiIcons


log = logging.getLogger(__name__)


class ThemeListWidgetItem(QtWidgets.QListWidgetItem):
    """
    Subclass a QListWidgetItem to allow dynamic loading of thumbnails from an online resource
    """
    def __init__(self, themes_url, sample_theme_data, ftw, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title = sample_theme_data['title']
        thumbnail = sample_theme_data['thumbnail']
        self.file_name = sample_theme_data['file_name']
        self.sha256 = sample_theme_data['sha256']
        self.setIcon(UiIcons().picture)  # Set a place holder icon whilst the thumbnails download
        self.setText(title)
        self.setToolTip(title)
        worker = DownloadWorker(themes_url, thumbnail)
        worker.download_failed.connect(self._on_download_failed)
        worker.download_succeeded.connect(self._on_thumbnail_downloaded)
        thread_name = 'thumbnail_download_{thumbnail}'.format(thumbnail=thumbnail)
        run_thread(worker, thread_name)
        ftw.thumbnail_download_threads.append(thread_name)

    def _on_download_failed(self):
        """
        Set an icon to indicate that the thumbnail download has failed.

        :rtype: None
        """
        self.setIcon(UiIcons().exception)

    def _on_thumbnail_downloaded(self, thumbnail_path):
        """
        Load the thumbnail as the icon when it has downloaded.

        :param Path thumbnail_path: Path to the file to use as a thumbnail
        :rtype: None
        """
        self.setIcon(build_icon(thumbnail_path))


class FirstTimeForm(QtWidgets.QWizard, UiFirstTimeWizard, RegistryProperties):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of OpenLP themes.
    """
    log.info('ThemeWizardForm loaded')

    def __init__(self, parent=None):
        """
        Create and set up the first time wizard.
        """
        super(FirstTimeForm, self).__init__(parent)
        self.web_access = True
        self.web = ''
        self.setup_ui(self)
        self.themes_list_widget.itemSelectionChanged.connect(self.on_themes_list_widget_selection_changed)
        self.themes_deselect_all_button.clicked.connect(self.themes_list_widget.clearSelection)
        self.themes_select_all_button.clicked.connect(self.themes_list_widget.selectAll)

    def get_next_page_id(self):
        """
        Returns the id of the next FirstTimePage to go to based on enabled plugins
        """
        if FirstTimePage.ScreenConfig < self.currentId() < FirstTimePage.Songs and self.songs_check_box.isChecked():
            # If the songs plugin is enabled then go to the songs page
            return FirstTimePage.Songs
        elif FirstTimePage.ScreenConfig < self.currentId() < FirstTimePage.Bibles and self.bible_check_box.isChecked():
            # Otherwise, if the Bibles plugin is enabled then go to the Bibles page
            return FirstTimePage.Bibles
        elif FirstTimePage.ScreenConfig < self.currentId() < FirstTimePage.Themes:
            # Otherwise, if the current page is somewhere between the Welcome and the Themes pages, go to the themes
            return FirstTimePage.Themes
        else:
            # If all else fails, go to the next page
            return self.currentId() + 1

    def nextId(self):
        """
        Determine the next page in the Wizard to go to.
        """
        self.application.process_events()
        if self.currentId() == FirstTimePage.Download:
            if not self.web_access:
                return FirstTimePage.NoInternet
            else:
                return FirstTimePage.Plugins
        elif self.currentId() == FirstTimePage.Plugins:
            return self.get_next_page_id()
        elif self.currentId() == FirstTimePage.Progress:
            return -1
        elif self.currentId() == FirstTimePage.NoInternet:
            return FirstTimePage.Progress
        return self.get_next_page_id()

    def exec(self):
        """
        Run the wizard.
        """
        self.set_defaults()
        return QtWidgets.QWizard.exec(self)

    def initialize(self, screens):
        """
        Set up the First Time Wizard

        :param screens: The screens detected by OpenLP
        """
        self.screens = screens
        self.was_cancelled = False
        self.thumbnail_download_threads = []
        self.has_run_wizard = False

    def _download_index(self):
        """
        Download the configuration file and kick off the theme screenshot download threads
        """
        # check to see if we have web access
        self.web_access = False
        self.config = ''
        web_config = None
        user_agent = 'OpenLP/' + Registry().get('application').applicationVersion()
        self.application.process_events()
        try:
            web_config = get_web_page('{host}{name}'.format(host=self.web, name='download_3.0.json'),
                                      headers={'User-Agent': user_agent})
        except ConnectionError:
            QtWidgets.QMessageBox.critical(self, translate('OpenLP.FirstTimeWizard', 'Network Error'),
                                           translate('OpenLP.FirstTimeWizard', 'There was a network error attempting '
                                                     'to connect to retrieve initial configuration information'),
                                           QtWidgets.QMessageBox.Ok)
        if web_config and self._parse_config(web_config):
            self.web_access = True
        self.application.process_events()
        self.downloading = translate('OpenLP.FirstTimeWizard', 'Downloading {name}...')
        self.application.set_normal_cursor()

    def _parse_config(self, web_config):
        try:
            config = json.loads(web_config)
            meta = config['_meta']
            self.web = meta['base_url']
            self.songs_url = self.web + meta['songs_dir'] + '/'
            self.bibles_url = self.web + meta['bibles_dir'] + '/'
            self.themes_url = self.web + meta['themes_dir'] + '/'
            for song in config['songs'].values():
                self.application.process_events()
                item = QtWidgets.QListWidgetItem(song['title'], self.songs_list_widget)
                item.setData(QtCore.Qt.UserRole, (song['file_name'], song['sha256']))
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            for lang in config['bibles'].values():
                self.application.process_events()
                lang_item = QtWidgets.QTreeWidgetItem(self.bibles_tree_widget, [lang['title']])
                for translation in lang['translations'].values():
                    self.application.process_events()
                    item = QtWidgets.QTreeWidgetItem(lang_item, [translation['title']])
                    item.setData(0, QtCore.Qt.UserRole, (translation['file_name'], translation['sha256']))
                    item.setCheckState(0, QtCore.Qt.Unchecked)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self.bibles_tree_widget.expandAll()
            self.application.process_events()
            for theme in config['themes'].values():
                ThemeListWidgetItem(self.themes_url, theme, self, self.themes_list_widget)
            self.application.process_events()
        except Exception:
            log.exception('Unable to parse sample config file %s', web_config)
            critical_error_message_box(
                translate('OpenLP.FirstTimeWizard', 'Invalid index file'),
                translate('OpenLP.FirstTimeWizard', 'OpenLP was unable to read the resource index file. '
                                                    'Please try again later.'))
            return False
        return True

    def set_defaults(self):
        """
        Set up display at start of theme edit.
        """
        self.restart()
        self.web = 'https://get.openlp.org/ftw/'
        self.cancel_button.clicked.connect(self.on_cancel_button_clicked)
        self.no_internet_finish_button.clicked.connect(self.on_no_internet_finish_button_clicked)
        self.no_internet_cancel_button.clicked.connect(self.on_no_internet_cancel_button_clicked)
        self.currentIdChanged.connect(self.on_current_id_changed)
        Registry().register_function('config_screen_changed', self.screen_selection_widget.load)
        self.no_internet_finish_button.setVisible(False)
        self.no_internet_cancel_button.setVisible(False)
        # Check if this is a re-run of the wizard.
        self.has_run_wizard = Settings().value('core/has run wizard')
        create_paths(Path(gettempdir(), 'openlp'))
        self.theme_combo_box.clear()
        if self.has_run_wizard:
            self.songs_check_box.setChecked(self.plugin_manager.get_plugin_by_name('songs').is_active())
            self.bible_check_box.setChecked(self.plugin_manager.get_plugin_by_name('bibles').is_active())
            self.presentation_check_box.setChecked(
                self.plugin_manager.get_plugin_by_name('presentations').is_active())
            self.image_check_box.setChecked(self.plugin_manager.get_plugin_by_name('images').is_active())
            self.media_check_box.setChecked(self.plugin_manager.get_plugin_by_name('media').is_active())
            self.custom_check_box.setChecked(self.plugin_manager.get_plugin_by_name('custom').is_active())
            self.song_usage_check_box.setChecked(self.plugin_manager.get_plugin_by_name('songusage').is_active())
            self.alert_check_box.setChecked(self.plugin_manager.get_plugin_by_name('alerts').is_active())
            # Add any existing themes to list.
            self.theme_combo_box.insertSeparator(0)
            self.theme_combo_box.addItems(sorted(self.theme_manager.get_themes()))
            default_theme = Settings().value('themes/global theme')
            # Pre-select the current default theme.
            index = self.theme_combo_box.findText(default_theme)
            self.theme_combo_box.setCurrentIndex(index)

    def on_current_id_changed(self, page_id):
        """
        Detects Page changes and updates as appropriate.
        """
        # Keep track of the page we are at.  Triggering "Cancel" causes page_id to be a -1.
        self.application.process_events()
        if page_id != -1:
            self.last_id = page_id
        if page_id == FirstTimePage.Download:
            self.back_button.setVisible(False)
            self.next_button.setVisible(False)
            # Set the no internet page text.
            if self.has_run_wizard:
                self.no_internet_label.setText(self.no_internet_text)
            else:
                self.no_internet_label.setText(self.no_internet_text + self.cancel_wizard_text)
            self.application.set_busy_cursor()
            self._download_index()
            self.application.set_normal_cursor()
            self.back_button.setVisible(False)
            self.next_button.setVisible(True)
            self.next()
        elif page_id == FirstTimePage.NoInternet:
            self.back_button.setVisible(False)
            self.next_button.setVisible(False)
            self.cancel_button.setVisible(False)
            self.no_internet_finish_button.setVisible(True)
            if self.has_run_wizard:
                self.no_internet_cancel_button.setVisible(False)
            else:
                self.no_internet_cancel_button.setVisible(True)
        elif page_id == FirstTimePage.Plugins:
            self.back_button.setVisible(False)
        elif page_id == FirstTimePage.Progress:
            self.application.set_busy_cursor()
            self._pre_wizard()
            self._perform_wizard()
            self._post_wizard()
            self.application.set_normal_cursor()

    def on_cancel_button_clicked(self):
        """
        Process the triggering of the cancel button.
        """
        self.was_cancelled = True
        if self.thumbnail_download_threads:  # TODO: Use main thread list
            for thread_name in self.thumbnail_download_threads:
                worker = get_thread_worker(thread_name)
                if worker:
                    worker.cancel_download()
        # Was the thread created.
        if self.thumbnail_download_threads:
            while any([not is_thread_finished(thread_name) for thread_name in self.thumbnail_download_threads]):
                time.sleep(0.1)
        self.application.set_normal_cursor()

    def on_themes_list_widget_selection_changed(self):
        """
        Update the `theme_combo_box` with the selected items

        :rtype: None
        """
        existing_themes = []
        if self.theme_manager:
            existing_themes = self.theme_manager.get_themes()
        for list_index in range(self.themes_list_widget.count()):
            item = self.themes_list_widget.item(list_index)
            if item.text() not in existing_themes:
                cbox_index = self.theme_combo_box.findText(item.text())
                if item.isSelected() and cbox_index == -1:
                    self.theme_combo_box.insertItem(0, item.text())
                elif not item.isSelected() and cbox_index != -1:
                    self.theme_combo_box.removeItem(cbox_index)

    def on_no_internet_finish_button_clicked(self):
        """
        Process the triggering of the "Finish" button on the No Internet page.
        """
        self.application.set_busy_cursor()
        self._perform_wizard()
        self.application.set_normal_cursor()
        Settings().setValue('core/has run wizard', True)
        self.close()

    def on_no_internet_cancel_button_clicked(self):
        """
        Process the triggering of the "Cancel" button on the No Internet page.
        """
        self.was_cancelled = True
        self.close()

    def update_progress(self, count, block_size):
        """
        Calculate and display the download progress. This method is called by download_file().
        """
        increment = (count * block_size) - self.previous_size
        self._increment_progress_bar(None, increment)
        self.previous_size = count * block_size

    def _increment_progress_bar(self, status_text, increment=1):
        """
        Update the wizard progress page.

        :param status_text: Current status information to display.
        :param increment: The value to increment the progress bar by.
        """
        if status_text:
            self.progress_label.setText(status_text)
        if increment > 0:
            self.progress_bar.setValue(self.progress_bar.value() + increment)
        self.application.process_events()

    def _pre_wizard(self):
        """
        Prepare the UI for the process.
        """
        self.max_progress = 0
        self.finish_button.setVisible(False)
        self.application.process_events()
        try:
            # Loop through the songs list and increase for each selected item
            for i in range(self.songs_list_widget.count()):
                self.application.process_events()
                item = self.songs_list_widget.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    filename, sha256 = item.data(QtCore.Qt.UserRole)
                    size = get_url_file_size('{path}{name}'.format(path=self.songs_url, name=filename))
                    self.max_progress += size
            # Loop through the Bibles list and increase for each selected item
            iterator = QtWidgets.QTreeWidgetItemIterator(self.bibles_tree_widget)
            while iterator.value():
                self.application.process_events()
                item = iterator.value()
                if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                    filename, sha256 = item.data(0, QtCore.Qt.UserRole)
                    size = get_url_file_size('{path}{name}'.format(path=self.bibles_url, name=filename))
                    self.max_progress += size
                iterator += 1
            # Loop through the themes list and increase for each selected item
            for item in self.themes_list_widget.selectedItems():
                size = get_url_file_size('{url}{file}'.format(url=self.themes_url, file=item.file_name))
                self.max_progress += size
        except urllib.error.URLError:
            trace_error_handler(log)
            critical_error_message_box(translate('OpenLP.FirstTimeWizard', 'Download Error'),
                                       translate('OpenLP.FirstTimeWizard', 'There was a connection problem during '
                                                 'download, so further downloads will be skipped. Try to re-run the '
                                                 'First Time Wizard later.'))
            self.max_progress = 0
            self.web_access = None
        if self.max_progress:
            # Add on 2 for plugins status setting plus a "finished" point.
            self.max_progress += 2
            self.progress_bar.setValue(0)
            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(self.max_progress)
            self.progress_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Setting Up And Downloading'))
            self.progress_page.setSubTitle(
                translate('OpenLP.FirstTimeWizard', 'Please wait while OpenLP is set up and your data is downloaded.'))
        else:
            self.progress_bar.setVisible(False)
            self.progress_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Setting Up'))
            self.progress_page.setSubTitle('Setup complete.')
        self.repaint()
        self.application.process_events()
        # Try to give the wizard a chance to repaint itself
        time.sleep(0.1)

    def _post_wizard(self):
        """
        Clean up the UI after the process has finished.
        """
        if self.max_progress:
            self.progress_bar.setValue(self.progress_bar.maximum())
            if self.has_run_wizard:
                text = translate('OpenLP.FirstTimeWizard',
                                 'Download complete. Click the {button} button to return to OpenLP.'
                                 ).format(button=clean_button_text(self.buttonText(QtWidgets.QWizard.FinishButton)))
                self.progress_label.setText(text)
            else:
                text = translate('OpenLP.FirstTimeWizard',
                                 'Download complete. Click the {button} button to start OpenLP.'
                                 ).format(button=clean_button_text(self.buttonText(QtWidgets.QWizard.FinishButton)))
                self.progress_label.setText(text)
        else:
            if self.has_run_wizard:
                text = translate('OpenLP.FirstTimeWizard',
                                 'Click the {button} button to return to OpenLP.'
                                 ).format(button=clean_button_text(self.buttonText(QtWidgets.QWizard.FinishButton)))
                self.progress_label.setText(text)
            else:
                text = translate('OpenLP.FirstTimeWizard',
                                 'Click the {button} button to start OpenLP.'
                                 ).format(button=clean_button_text(self.buttonText(QtWidgets.QWizard.FinishButton)))
                self.progress_label.setText(text)
        self.finish_button.setVisible(True)
        self.finish_button.setEnabled(True)
        self.cancel_button.setVisible(False)
        self.next_button.setVisible(False)
        self.application.process_events()

    def _perform_wizard(self):
        """
        Run the tasks in the wizard.
        """
        # Set plugin states
        self._increment_progress_bar(translate('OpenLP.FirstTimeWizard', 'Enabling selected plugins...'))
        self._set_plugin_status(self.songs_check_box, 'songs/status')
        self._set_plugin_status(self.bible_check_box, 'bibles/status')
        self._set_plugin_status(self.presentation_check_box, 'presentations/status')
        self._set_plugin_status(self.image_check_box, 'images/status')
        self._set_plugin_status(self.media_check_box, 'media/status')
        self._set_plugin_status(self.custom_check_box, 'custom/status')
        self._set_plugin_status(self.song_usage_check_box, 'songusage/status')
        self._set_plugin_status(self.alert_check_box, 'alerts/status')
        if self.web_access:
            if not self._download_selected():
                critical_error_message_box(translate('OpenLP.FirstTimeWizard', 'Download Error'),
                                           translate('OpenLP.FirstTimeWizard', 'There was a connection problem while '
                                                     'downloading, so further downloads will be skipped. Try to re-run '
                                                     'the First Time Wizard later.'))
        self.screen_selection_widget.save()
        if self.theme_combo_box.currentIndex() != -1:
            Settings().setValue('themes/global theme', self.theme_combo_box.currentText())

    def _download_selected(self):
        """
        Download selected songs, bibles and themes. Returns False on download error
        """
        # Build directories for downloads
        songs_destination_path = Path(gettempdir(), 'openlp')
        bibles_destination_path = AppLocation.get_section_data_path('bibles')
        themes_destination_path = AppLocation.get_section_data_path('themes')
        missed_files = []
        # Download songs
        for i in range(self.songs_list_widget.count()):
            item = self.songs_list_widget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                filename, sha256 = item.data(QtCore.Qt.UserRole)
                self._increment_progress_bar(self.downloading.format(name=filename), 0)
                self.previous_size = 0
                destination = songs_destination_path / str(filename)
                if not download_file(self, '{path}{name}'.format(path=self.songs_url, name=filename),
                                     destination, sha256):
                    missed_files.append('Song: {name}'.format(name=filename))
        # Download Bibles
        bibles_iterator = QtWidgets.QTreeWidgetItemIterator(self.bibles_tree_widget)
        while bibles_iterator.value():
            item = bibles_iterator.value()
            if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                bible, sha256 = item.data(0, QtCore.Qt.UserRole)
                self._increment_progress_bar(self.downloading.format(name=bible), 0)
                self.previous_size = 0
                if not download_file(self, '{path}{name}'.format(path=self.bibles_url, name=bible),
                                     bibles_destination_path / bible, sha256):
                    missed_files.append('Bible: {name}'.format(name=bible))
            bibles_iterator += 1
        # Download themes
        for item in self.themes_list_widget.selectedItems():
            self._increment_progress_bar(self.downloading.format(name=item.file_name), 0)
            self.previous_size = 0
            if not download_file(self, '{url}{file}'.format(url=self.themes_url, file=item.file_name),
                                 themes_destination_path / item.file_name, item.sha256):
                missed_files.append('Theme: name'.format(name=item.file_name))
        if missed_files:
            file_list = ''
            for entry in missed_files:
                file_list += '{text}<br \\>'.format(text=entry)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle(translate('OpenLP.FirstTimeWizard', 'Network Error'))
            msg.setText(translate('OpenLP.FirstTimeWizard', 'Unable to download some files'))
            msg.setInformativeText(translate('OpenLP.FirstTimeWizard',
                                             'The following files were not able to be '
                                             'downloaded:<br \\>{text}'.format(text=file_list)))
            msg.setStandardButtons(msg.Ok)
            msg.exec()
        return True

    def _set_plugin_status(self, field, tag):
        """
        Set the status of a plugin.
        """
        status = PluginStatus.Active if field.checkState() == QtCore.Qt.Checked else PluginStatus.Inactive
        Settings().setValue(tag, status)
