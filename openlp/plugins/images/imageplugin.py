# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import logging

from openlp.core.lib import Plugin, buildIcon
from openlp.plugins.images.lib import ImageMediaItem, ImageTab

class ImagePlugin(Plugin):
    global log
    log = logging.getLogger(u'ImagePlugin')
    log.info(u'Image Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Images', u'1.9.0', plugin_helpers)
        self.weight = -7
        self.icon = buildIcon(u':/media/media_image.png')

    def can_be_disabled(self):
        return True

    def initialise(self):
        log.info(u'Plugin Initialising')
        Plugin.initialise(self)
        self.insert_toolbox_item()

    def finalise(self):
        log.info(u'Plugin Finalise')
        self.remove_toolbox_item()

    def get_settings_tab(self):
        return ImageTab(self.name)

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        return ImageMediaItem(self, self.icon, self.name)

    def about(self):
        about_text = self.trUtf8(u'<b>Image Plugin</b><br>Allows images of '
            u'all types to be displayed.  If a number of images are selected '
            u'together and presented on the live controller it is possible '
            u'to turn them into a timed loop.<br>From the plugin if the '
            u'<i>Override background</i> is chosen and an image is selected '
            u'any somgs which are rendered will use the selected image from '
            u'the background instead of the one provied by the theme.<br>')
        return about_text
