#!/usr/bin/env python
import gtk,time,threading,os,signal

k = threading.Thread(target=gtk.main)

class myStatusIcon(gtk.StatusIcon):
	def __init__(self):
		gtk.StatusIcon.__init__(self)
def activate(self):
	print "Activated!"
def doquit(self):
	print "Quitting!"
	os.kill(os.getpid(),signal.SIGTERM)
	
def popup(self,button,activate_time):
	print "Creating the menu"
	pop = gtk.Menu()
	quit = gtk.MenuItem("Quit")
	quit.connect("activate",doquit)
	pop.append(quit)
	pop.show_all()
	pop.popup(None,None,None,button,activate_time,None)

gtk.gdk.threads_init()
n = myStatusIcon()
n.connect("activate",activate)
n.connect("popup-menu",popup)
n.set_from_file("/usr/share/pixmaps/gwibber.svg")
n.set_tooltip_text("Egg-Wireless")

k.start()
