"""
    Package to test the openlp.core.ui package.
"""
import sys
from unittest import TestCase

from mock import MagicMock, patch
from openlp.core.ui import starttimeform
from PyQt4 import QtCore, QtGui, QtTest

class TestStartTimeDialog(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        self.app = QtGui.QApplication([])
        self.window = QtGui.QMainWindow()
        self.form = starttimeform.StartTimeForm(self.window)

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.window
        del self.app

    def ui_defaults_test(self):
        """
        Test StartTimeDialog defaults
        """
        self.assertEqual(self.form.hourSpinBox.minimum(), 0)
        self.assertEqual(self.form.hourSpinBox.maximum(), 4)
        self.assertEqual(self.form.minuteSpinBox.minimum(), 0)
        self.assertEqual(self.form.minuteSpinBox.maximum(), 59)
        self.assertEqual(self.form.secondSpinBox.minimum(), 0)
        self.assertEqual(self.form.secondSpinBox.maximum(), 59)
        self.assertEqual(self.form.hourFinishSpinBox.minimum(), 0)
        self.assertEqual(self.form.hourFinishSpinBox.maximum(), 4)
        self.assertEqual(self.form.minuteFinishSpinBox.minimum(), 0)
        self.assertEqual(self.form.minuteFinishSpinBox.maximum(), 59)
        self.assertEqual(self.form.secondFinishSpinBox.minimum(), 0)
        self.assertEqual(self.form.secondFinishSpinBox.maximum(), 59)

    def time_display_test(self):
        """
        Test StartTimeDialog display initialisation
        """
        # GIVEN: A service item with with time
        mocked_serviceitem = MagicMock()
        mocked_serviceitem.start_time = 61
        mocked_serviceitem.end_time = 3701
        mocked_serviceitem.media_length = 3701

        # WHEN displaying the UI and pressing enter
        self.form.item = {u'service_item': mocked_serviceitem}
        with patch(u'PyQt4.QtGui.QDialog') as mocked_exec:
            self.form.exec_()
        okWidget = self.form.buttonBox.button(self.form.buttonBox.Ok)
        QtTest.QTest.mouseClick(okWidget, QtCore.Qt.LeftButton)

        # THEN the following input values values are returned
        self.assertEqual(self.form.hourSpinBox.value(), 0)
        self.assertEqual(self.form.minuteSpinBox.value(), 1)
        self.assertEqual(self.form.secondSpinBox.value(), 1)
        self.assertEqual(self.form.item[u'service_item'].start_time, 61, u'The start time has not changed')

        # WHEN displaying the UI, changing the time to 2min 3secs and pressing enter
        self.form.item = {u'service_item': mocked_serviceitem}
        with patch(u'PyQt4.QtGui.QDialog') as mocked_exec:
            self.form.exec_()
        self.form.minuteSpinBox.setValue(2)
        self.form.secondSpinBox.setValue(3)
        okWidget = self.form.buttonBox.button(self.form.buttonBox.Ok)
        QtTest.QTest.mouseClick(okWidget, QtCore.Qt.LeftButton)

        # THEN the following values values are returned
        self.assertEqual(self.form.hourSpinBox.value(), 0)
        self.assertEqual(self.form.minuteSpinBox.value(), 2)
        self.assertEqual(self.form.secondSpinBox.value(), 3)
        self.assertEqual(self.form.item[u'service_item'].start_time, 123, u'The start time has changed')