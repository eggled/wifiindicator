#!/usr/bin/env python


## Import this file & use it to execute a callback, every time /var/run/wpa_supplicant/wlan0 appears
## (i.e. the callback should reconnect the socket).  See USAGE below.

import pyinotify,os,re,sys
import logging

pyinotify.log.setLevel(logging.CRITICAL)

class PE (pyinotify.ProcessEvent):
	def process_IN_ATTRIB(self,event):
		if event.pathname == "/var/run/wpa_supplicant":
			self.wm.add_watch("/var/run/wpa_supplicant",pyinotify.ALL_EVENTS,proc_fun=self,auto_add=True)
			if os.path.exists("/var/run/wpa_supplicant/wlan0"):
				self.callback()
	def process_IN_CREATE(self,event):
		if event.pathname == "/var/run/wpa_supplicant/wlan0":
			self.callback()

"""
# USAGE:

import inotify
def cb():
	print "Gotcha"

inotify.initwatch(cb)
## Suggest executing this in a thread or something...
"""

def initwatch(callback):
	processor = PE()
	processor.callback = callback
	wm = pyinotify.WatchManager()
	processor.wm = wm
	wm.add_watch("/var/run",pyinotify.ALL_EVENTS,proc_fun=processor,auto_add=True)
	notifier = pyinotify.Notifier(wm)
	try:
		notifier.loop()
	except pyinotify.ProcessEventError:
		pass
