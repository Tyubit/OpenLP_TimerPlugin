"""
Package to test the openlp.core.lib.settingsform package.
"""
from unittest import TestCase

from mock import MagicMock, patch

from PyQt4 import QtCore, QtTest

from openlp.core.ui import settingsform
from openlp.core.lib import Registry, ScreenList


SCREEN = {
    u'primary': False,
    u'number': 1,
    u'size': QtCore.QRect(0, 0, 1024, 768)
}


class TestSettingsForm(TestCase):
    """
    Test the PluginManager class
    """

    def setUp(self):
        """
        Some pre-test setup required.
        """
        self.desktop = MagicMock()
        self.desktop.primaryScreen.return_value = SCREEN[u'primary']
        self.desktop.screenCount.return_value = SCREEN[u'number']
        self.desktop.screenGeometry.return_value = SCREEN[u'size']
        self.screens = ScreenList.create(self.desktop)
        Registry.create()
        self.form = settingsform.SettingsForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form

    def basic_cancel_test(self):
        """
        Test running the settings form and pressing Cancel
        """
        # GIVEN: An initial form

        # WHEN displaying the UI and pressing cancel
        with patch(u'PyQt4.QtGui.QDialog.reject') as mocked_reject:
            cancel_widget = self.form.button_box.button(self.form.button_box.Cancel)
            QtTest.QTest.mouseClick(cancel_widget, QtCore.Qt.LeftButton)

            # THEN the dialog reject should have been called
            assert mocked_reject.call_count == 1, u'The QDialog.reject should have been called'

    def basic_accept_test(self):
        """
        Test running the settings form and pressing Ok
        """
        # GIVEN: An initial form

        # WHEN displaying the UI and pressing Ok
        with patch(u'PyQt4.QtGui.QDialog.accept') as mocked_accept:
            ok_widget = self.form.button_box.button(self.form.button_box.Ok)
            QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

            # THEN the dialog reject should have been called
            assert mocked_accept.call_count == 1, u'The QDialog.accept should have been called'

    def basic_register_test(self):
        """
        Test running the settings form and adding a single function
        """
        # GIVEN: An initial form add a register function
        self.form.register_post_process(u'function1')

        # WHEN displaying the UI and pressing Ok
        with patch(u'PyQt4.QtGui.QDialog.accept'):
            ok_widget = self.form.button_box.button(self.form.button_box.Ok)
            QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

            # THEN the processing stack should be empty
            assert len(self.form.processes) == 0, u'The one requested process should have been removed from the stack'

    def register_multiple_functions_test(self):
        """
        Test running the settings form and adding multiple functions
        """
        # GIVEN: Registering a single function
        self.form.register_post_process(u'function1')

        # WHEN testing the processing stack
        # THEN the processing stack should have one item
        assert len(self.form.processes) == 1, u'The one requested process should have been added to the stack'

        # GIVEN: Registering a new function
        self.form.register_post_process(u'function2')

        # WHEN testing the processing stack
        # THEN the processing stack should have two items
        assert len(self.form.processes) == 2, u'The two requested processes should have been added to the stack'

        # GIVEN: Registering a process for the second time
        self.form.register_post_process(u'function1')

        # WHEN testing the processing stack
        # THEN the processing stack should still have two items
        assert len(self.form.processes) == 2, u'No new processes should have been added to the stack'

    def register_multiple_functions_test(self):
        """
        Test running the settings form and adding multiple functions
        """
        # GIVEN: Three functions registered to be call
        dummy1 = MagicMock()
        dummy2 = MagicMock()
        dummy3 = MagicMock()

        Registry().register_function(u'images_config_updated', dummy1)
        Registry().register_function(u'config_screen_changed', dummy2)
        Registry().register_function(u'images_regenerate', dummy3)

        # WHEN: The Images have been changed and the form sumbitted
        self.form.register_post_process(u'images_config_updated')
        self.form.accept()

        # THEN Images_regenerate should have been called.
        assert dummy1.call_count == 1, u'dummy1 should have been called once'
        assert dummy2.call_count == 0, u'dummy2 should not have been called once'
        assert dummy3.call_count == 1, u'dummy3 should have been called once'

        # WHEN: The Images have been changed and the form submitted
        dummy1.reset_mock()
        dummy2.reset_mock()
        dummy3.reset_mock()
        self.form.register_post_process(u'config_screen_changed')
        self.form.accept()

        # THEN Images_regenerate should have been called.
        assert dummy1.call_count == 0, u'dummy1 should not have been called once'
        assert dummy2.call_count == 1, u'dummy2 should have been called once'
        assert dummy3.call_count == 1, u'dummy3 should have been called once'

        # WHEN: The Images have been changed and the form submitted
        dummy1.reset_mock()
        dummy2.reset_mock()
        dummy3.reset_mock()
        self.form.register_post_process(u'config_screen_changed')
        self.form.register_post_process(u'images_config_updated')
        self.form.accept()

        # THEN Images_regenerate should have been called.
        assert dummy1.call_count == 1, u'dummy1 should have been called once'
        assert dummy2.call_count == 1, u'dummy2 should have been called once'
        assert dummy3.call_count == 1, u'dummy3 should have been called once'