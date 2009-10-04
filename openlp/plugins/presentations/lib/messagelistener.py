# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import logging
import os

from PyQt4 import QtCore

from openlp.core.lib import Receiver

class MessageListener(object):
    """
    This is the Presentation listener who acts on events from the slide
    controller and passes the messages on the the correct presentation handlers
    """
    global log
    log = logging.getLogger(u'MessageListener')
    log.info(u'Message Listener loaded')

    def __init__(self, controllers):
        self.controllers = controllers
        self.handler = None
        # messages are sent from core.ui.slidecontroller
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_start'), self.startup)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_stop'), self.shutdown)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_first'), self.first)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_previous'), self.previous)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_next'), self.next)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_last'), self.last)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_slide'), self.slide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_blank'), self.blank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_unblank'), self.unblank)

    def startup(self, message):
        """
        Start of new presentation
        Save the handler as any new presentations start here
        """
        self.handler, file = self.decodeMessage(message)
        self.controller = self.controllers[self.handler]
        if self.controller.is_loaded():
            self.shutdown()
        self.controller.load_presentation(file)

    def slide(self, message):
        #if not self.controller.is_loaded():
        #    return
        #if not self.controller.is_active():
        #    self.controller.start_presentation()
        self.controller.goto_slide(message[0])

    def first(self, message):
        """
        Based on the handler passed at startup triggers the first slide
        """
        #if not self.controller.is_loaded():
        #    return
        self.controller.start_presentation()

    def last(self, message):
        """
        Based on the handler passed at startup triggers the first slide
        """
        #if not self.controller.is_loaded():
        #    return
        #if not self.controller.is_active():
        #    self.controller.start_presentation()
        self.controller.goto_slide(self.controller.get_slide_count())

    def next(self, message):
        """
        Based on the handler passed at startup triggers the next slide event
        """
        #if not self.controller.is_loaded():
        #    return
        #if not self.controller.is_active():
        #    self.controller.start_presentation()
        #    self.controller.goto_slide(self.controller.current_slide)
        self.controller.next_step()

    def previous(self, message):
        """
        Based on the handler passed at startup triggers the previous slide event
        """
        #if not self.controller.is_loaded():
        #    return
        #if not self.controller.is_active():
        #    self.controller.start_presentation()
        #    self.controller.goto_slide(self.controller.current_slide)
        self.controller.previous_step()

    def shutdown(self, message):
        """
        Based on the handler passed at startup triggers slide show to shut down
        """
        self.controller.close_presentation()

    def blank(self):
        #if not self.controller.is_loaded():
        #    return
        #if not self.controller.is_active():
        #    self.controller.start_presentation()
        self.controller.blank_screen()        

    def unblank(self):
        #if not self.controller.is_loaded():
        #    return
        #if not self.controller.is_active():
        #    self.controller.start_presentation()
        self.controller.unblank_screen()        

    def decodeMessage(self, message):
        """
        Splits the message from the SlideController into it's component parts

        ``message``
        Message containing Presentaion handler name and file to be presented.
        """
        file = os.path.join(message[1], message[2])
        return message[0], file
