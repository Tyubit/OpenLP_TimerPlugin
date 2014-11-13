# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
Package to test the openlp.core.lib.settings package.
"""
from unittest import TestCase

from openlp.core.common import Settings
from tests.helpers.testmixin import TestMixin


class TestSettings(TestCase, TestMixin):
    """
    Test the functions in the Settings module
    """
    def setUp(self):
        """
        Create the UI
        """
        self.setup_application()
        self.build_settings()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.destroy_settings()

    def settings_basic_test(self):
        """
        Test the Settings creation and its default usage
        """
        # GIVEN: A new Settings setup

        # WHEN reading a setting for the first time
        default_value = Settings().value('core/has run wizard')

        # THEN the default value is returned
        self.assertFalse(default_value, 'The default value should be False')

        # WHEN a new value is saved into config
        Settings().setValue('core/has run wizard', True)

        # THEN the new value is returned when re-read
        self.assertTrue(Settings().value('core/has run wizard'), 'The saved value should have been returned')

    def settings_override_test(self):
        """
        Test the Settings creation and its override usage
        """
        # GIVEN: an override for the settings
        screen_settings = {
            'test/extend': 'very wide',
        }
        Settings().extend_default_settings(screen_settings)

        # WHEN reading a setting for the first time
        extend = Settings().value('test/extend')

        # THEN the default value is returned
        self.assertEqual('very wide', extend, 'The default value of "very wide" should be returned')

        # WHEN a new value is saved into config
        Settings().setValue('test/extend', 'very short')

        # THEN the new value is returned when re-read
        self.assertEqual('very short', Settings().value('test/extend'), 'The saved value should be returned')

    def settings_override_with_group_test(self):
        """
        Test the Settings creation and its override usage - with groups
        """
        # GIVEN: an override for the settings
        screen_settings = {
            'test/extend': 'very wide',
        }
        Settings.extend_default_settings(screen_settings)

        # WHEN reading a setting for the first time
        settings = Settings()
        settings.beginGroup('test')
        extend = settings.value('extend')

        # THEN the default value is returned
        self.assertEqual('very wide', extend, 'The default value defined should be returned')

        # WHEN a new value is saved into config
        Settings().setValue('test/extend', 'very short')

        # THEN the new value is returned when re-read
        self.assertEqual('very short', Settings().value('test/extend'), 'The saved value should be returned')

    def settings_nonexisting_test(self):
        """
        Test the Settings on query for non-existing value
        """
        # GIVEN: A new Settings setup
        with self.assertRaises(KeyError) as cm:
            # WHEN reading a setting that doesn't exists
            does_not_exist_value = Settings().value('core/does not exists')

        # THEN: An exception with the non-existing key should be thrown
        self.assertEqual(str(cm.exception), "'core/does not exists'", 'We should get an exception')
