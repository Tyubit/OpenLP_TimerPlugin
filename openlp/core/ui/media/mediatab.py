# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2019 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
The :mod:`~openlp.core.ui.media.mediatab` module holds the configuration tab for the media stuff.
"""
import logging

from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QCameraInfo, QAudioDeviceInfo, QAudio

from openlp.core.common import is_linux, is_win
from openlp.core.common.i18n import translate
from openlp.core.common.settings import Settings
from openlp.core.lib.settingstab import SettingsTab
from openlp.core.ui.icons import UiIcons

LINUX_STREAM = 'v4l2://{video} :v4l2-standard= :input-slave={audio} :live-caching=300'
WIN_STREAM = 'dshow://:dshow-vdev={video} :dshow-adev={audio} :live-caching=300'
OSX_STREAM = 'avcapture://{video} :qtsound://{audio} :live-caching=300'

log = logging.getLogger(__name__)


class MediaTab(SettingsTab):
    """
    MediaTab is the Media settings tab in the settings dialog.
    """
    def __init__(self, parent):
        """
        Constructor
        """
        self.icon_path = UiIcons().video
        player_translated = translate('OpenLP.MediaTab', 'Media')
        super(MediaTab, self).__init__(parent, 'Media', player_translated)

    def setup_ui(self):
        """
        Set up the UI
        """
        self.setObjectName('MediaTab')
        super(MediaTab, self).setup_ui()
        self.live_media_group_box = QtWidgets.QGroupBox(self.left_column)
        self.live_media_group_box.setObjectName('live_media_group_box')
        self.media_layout = QtWidgets.QVBoxLayout(self.live_media_group_box)
        self.media_layout.setObjectName('live_media_layout')
        self.auto_start_check_box = QtWidgets.QCheckBox(self.live_media_group_box)
        self.auto_start_check_box.setObjectName('auto_start_check_box')
        self.media_layout.addWidget(self.auto_start_check_box)
        self.left_layout.addWidget(self.live_media_group_box)
        self.stream_media_group_box = QtWidgets.QGroupBox(self.left_column)
        self.stream_media_group_box.setObjectName('stream_media_group_box')
        self.stream_media_layout = QtWidgets.QHBoxLayout(self.stream_media_group_box)
        self.stream_media_layout.setObjectName('stream_media_layout')
        self.stream_media_layout.setContentsMargins(0, 0, 0, 0)
        self.stream_edit = QtWidgets.QLabel(self)
        self.stream_media_layout.addWidget(self.stream_edit)
        self.left_layout.addWidget(self.stream_media_group_box)
        self.vlc_additions_group_box = QtWidgets.QGroupBox(self.left_column)
        self.vlc_additions_group_box.setObjectName('vlc_additions_group_box')
        self.vlc_additions_layout = QtWidgets.QHBoxLayout(self.vlc_additions_group_box)
        self.vlc_additions_layout.setObjectName('vlc_additions_layout')
        self.vlc_additions_layout.setContentsMargins(0, 0, 0, 0)
        self.vlc_additions_edit = QtWidgets.QPlainTextEdit(self)
        self.vlc_additions_layout.addWidget(self.vlc_additions_edit)
        self.left_layout.addWidget(self.vlc_additions_group_box)
        self.left_layout.addStretch()
        self.right_layout.addStretch()
        # # Signals and slots

    def retranslate_ui(self):
        """
        Translate the UI on the fly
        """
        self.live_media_group_box.setTitle(translate('MediaPlugin.MediaTab', 'Live Media'))
        self.stream_media_group_box.setTitle(translate('MediaPlugin.MediaTab', 'Stream Media Command'))
        self.vlc_additions_group_box.setTitle(translate('MediaPlugin.MediaTab', 'VLC additional commands'))
        self.auto_start_check_box.setText(translate('MediaPlugin.MediaTab', 'Start Live items automatically'))

    def load(self):
        """
        Load the settings
        """
        self.auto_start_check_box.setChecked(Settings().value(self.settings_section + '/media auto start'))
        self.stream_edit.setText(Settings().value(self.settings_section + '/stream command'))
        if not self.stream_edit.text():
            if is_linux:
                self.stream_edit.setText(LINUX_STREAM)
            elif is_win:
                self.stream_edit.setText(WIN_STREAM)
            else:
                self.stream_edit.setText(OSX_STREAM)
        self.vlc_additions_edit.setPlainText(Settings().value(self.settings_section + '/vlc additions'))
        if Settings().value('advanced/experimental'):
            for cam in QCameraInfo.availableCameras():
                log.debug(cam.deviceName())
                log.debug(cam.description())
            for au in QAudioDeviceInfo.availableDevices(QAudio.AudioInput):
                log.debug(au.deviceName())

    def save(self):
        """
        Save the settings
        """
        setting_key = self.settings_section + '/media auto start'
        if Settings().value(setting_key) != self.auto_start_check_box.checkState():
            Settings().setValue(setting_key, self.auto_start_check_box.checkState())
        Settings().setValue(self.settings_section + '/stream command', self.stream_edit.text())
        Settings().setValue(self.settings_section + '/vlc additions', self.vlc_additions_edit.toPlainText())

    def post_set_up(self, post_update=False):
        """
        Late setup for players as the MediaController has to be initialised first.

        :param post_update: Indicates if called before or after updates.
        """
        pass

    def on_revert(self):
        pass
