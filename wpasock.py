#!/usr/bin/env python

import socket,os,sys

def bssidHandle(val):
	return
def ssidHandle(val):
	return
def mgmtHandle(val):
	return
def stateHandle(val):
	return
def ipHandle(val):
	return

retvals={'bssid':bssidHandle,
	 'ssid':ssidHandle,
	 'key_mgmt':mgmtHandle,
	 'wpa_state':stateHandle,
	 'ip_address':ipHandle}

g =socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM,0)

g.connect("/var/run/wpa_supplicant/wlan0")
g.bind("/tmp/%d" % os.getpid())

g.send("STATUS""STATUS")

print g.recv(65535)
