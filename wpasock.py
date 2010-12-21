#!/usr/bin/env python

import socket,os,sys,re,threading,inotify,time,ind


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
		try:
			data = self.sock.recv(65535)
		except:
			try:
				self.sock.send("PING")
			except:
				pass
			try:
				data = self.sock.recv(65535)
			except:
				self.setstate("DISCONNECTED")
				return
		splitdata = re.split("[\r\n]+",data)
		for line in splitdata:
			try:
				key,data = re.split("=",line)
			except ValueError:
				if re.search("CTRL-EVENT-CONNECTED",line):
					self.sock.send("STATUS")
					self.runparse()
				continue
			if key in self.fnmap:
				self.fnmap[key](data)
			
	def setssid(self,ssid):
		self.ssid = ssid
	def setkeymgmt(self,mgmt):
		self.keymgmt = mgmt
	def setstate(self,state):	
		self.state = state
		if state != "COMPLETED":
			self.bssid=""
			self.ssid=""
			self.keymgmt = ""
			self.ip = ""
			self.qual = ""
			ind.n.set_from_file("icon/wifi0.png")
	def setip(self,ip):
		self.ip = ip
		self.setqual(self.qual)
	def setqual(self,qual):
		self.qual = qual
		qual = int(qual,10)
		if self.ip == "":
			ind.n.set_from_file("icon/wifi0.png")
		elif qual < 25:
			ind.n.set_from_file("icon/wifi1.png")
		elif qual < 50:
			ind.n.set_from_file("icon/wifi2.png")
		elif qual < 75:
			ind.n.set_from_file("icon/wifi3.png")
		else:
			ind.n.set_from_file("icon/wifi4.png")
	def __str__(self):
		return "%s: \nssid: %s\nqual: %s\naddr: %s\nproto: %s" % (self.state, self.ssid, self.qual, self.ip, self.keymgmt)
	def __repr__(self):
		return str(self)
	def doconnect(self,path):
		try:
			if not self.sock:
				self.sock =socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM,0)
				self.sock.bind("/tmp/%d" % os.getpid())
			self.sock.connect(path)
			self.sock.send("ATTACH")
			self.sock.send("STATUS")
			self.sock.settimeout(1)
			self.runparse()
		except:
			time.sleep(0.5)
			self.doconnect(path)
	def lackingData(self):
		if self.state != "COMPLETED":
			return None
		if not self.ip or not self.qual or not self.bssid:
			return 1
		if not self.ssid or not self.keymgmt:
			return 1
wpamon = wpaclass()
def establish():
	wpamon.doconnect("/var/run/wpa_supplicant/wlan0")
establish()
th = threading.Thread(target=inotify.initwatch,kwargs={'callback':establish})
th.start()
while 1:
	wpamon.runparse()
	ind.n.set_tooltip_text(str(wpamon))
	if wpamon.lackingData():
		time.sleep(1) ## Limit how often we'll update
		wpamon.sock.send("STATUS")
wpamon.sock.shutdown(socket.SHUT_RDWR)
os.remove("/tmp/%d" % os.getpid())
