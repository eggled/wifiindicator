#!/usr/bin/env python

import socket,os,sys,re

def bssidHandle(val):
	wpamon.setbssid(val)
	return
def ssidHandle(val):
	wpamon.setssid(val)
	return
def mgmtHandle(val):
	wpamon.setkeymgmt(val)
	return
def stateHandle(val):
	wpamon.setstate(val)
	return
def ipHandle(val):
	wpamon.setip(val)
	return
def qualHandle(val):
	wpamon.setqual(val)
	return

def doparse(val):
	try:
		key,data = re.split("=",val)
	except ValueError:
		return
	if key in retvals:
		retvals[key](data)

class wpaclass:
	def __init__(self):
		self.bssid = ""
		self.ssid = ""
		self.keymgmt = ""
		self.state = ""
		self.ip = ""
		self.qual = ""
		self.sock = None
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
			doparse(line)
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
		
		

retvals={'bssid':bssidHandle,
	 'ssid':ssidHandle,
	 'key_mgmt':mgmtHandle,
	 'wpa_state':stateHandle,
	 'ip_address':ipHandle,
	 'qual':qualHandle}

wpamon = wpaclass()
wpamon.sock =socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM,0)

wpamon.sock.connect("/var/run/wpa_supplicant/wlan0")
wpamon.sock.bind("/tmp/%d" % os.getpid())

wpamon.sock.send("STATUS")
wpamon.runparse()
print wpamon

os.remove("/tmp/%d" % os.getpid())
