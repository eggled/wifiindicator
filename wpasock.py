#!/usr/bin/env python

import socket,os,sys,re


class wpaclass:
	def __init__(self):
		self.bssid = ""
		self.ssid = ""
		self.keymgmt = ""
		self.state = ""
		self.ip = ""
		self.qual = ""
		self.sock = None
		self.fnmap={'bssid':self.setbssid,
			    'ssid':self.setssid,
			    'key_mgmt':self.setkeymgmt,
			    'wpa_state':self.setstate,
			    'ip_address':self.setip,
			    'qual':self.setqual}
		return
	def setbssid(self,bssid):
		if bssid != self.bssid:
			self.bssid = bssid
			if self.sock:
				self.sock.send("BSS %s" % bssid)
				self.runparse()
	def runparse(self):
		data = self.sock.recv(65535)
		splitdata = re.split("[\r\n]+",data)
		for line in splitdata:
			try:
				key,data = re.split("=",line)
			except ValueError:
				continue
			if key in self.fnmap:
				self.fnmap[key](data)
			
	def setssid(self,ssid):
		self.ssid = ssid
	def setkeymgmt(self,mgmt):
		self.keymgmt = mgmt
	def setstate(self,state):	
		self.state = state
	def setip(self,ip):
		self.ip = ip
	def setqual(self,qual):
		self.qual = qual
	def __str__(self):
		return "%s: Connected to %s strength %s, ip %s, proto %s" % (self.state, self.ssid, self.qual, self.ip, self.keymgmt)
	def __repr__(self):
		return str(self)
		
		
wpamon = wpaclass()
wpamon.sock =socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM,0)

wpamon.sock.connect("/var/run/wpa_supplicant/wlan0")
wpamon.sock.bind("/tmp/%d" % os.getpid())

wpamon.sock.send("STATUS")
wpamon.runparse()
print wpamon
while 1:
	wpamon.runparse()
	print wpamon
wpamon.sock.shutdown(socket.SHUT_RDWR)
os.remove("/tmp/%d" % os.getpid())
