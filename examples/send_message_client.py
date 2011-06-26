#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import traceback
import sys
import logging
from getpass import getpass

from pyxmpp2.jid import JID
from pyxmpp2.message import Message
from pyxmpp2.client import Client
from pyxmpp2.settings import XMPPSettings
from pyxmpp2.mainloop.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent

class MyHandler(EventHandler):
    def __init__(self, target_jid, message):
        self.target_jid = target_jid
        self.message = message

    @event_handler(AuthorizedEvent)
    def handle_authorized(self, event):
        message = Message(to_jid = self.target_jid, body = self.message)
        event.stream.send(message)
        event.stream.disconnect()

    @event_handler(DisconnectedEvent)
    def handle_disconnected(self, event):
        return QUIT
    
    @event_handler()
    def handle_all(self, event):
        logger.info(u"-- {0}".format(event))

logger=logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

your_jid = raw_input("Your jid: ").decode("utf-8")
your_password = getpass("Your password: ")
target_jid = raw_input("Target jid: ")
message = raw_input("Message: ")

if sys.version_info.major < 3:
    your_jid = your_jid.decode("utf-8")
    your_password = your_password.decode("utf-8")
    target_jid = target_jid.decode("utf-8")
    message = message.decode("utf-8")

handler = MyHandler(JID(target_jid), message)
settings = XMPPSettings({"password": your_password})
client = Client(JID(your_jid), [handler], settings)
client.connect()
client.run()

