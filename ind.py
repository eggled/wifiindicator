#!/usr/bin/env python
import gtk,time,threading,os,signal

def watchwpa():
	print "Doing my sleeping"
	watchwpa.n.set_from_file("icon/wifi0.png")
	time.sleep(2)
	watchwpa.n.set_from_file("icon/wifi1.png")
	time.sleep(2)
	watchwpa.n.set_from_file("icon/wifi2.png")
	time.sleep(2)
	watchwpa.n.set_from_file("icon/wifi3.png")
	time.sleep(2)
	watchwpa.n.set_from_file("icon/wifi4.png")
	time.sleep(2)
	print "All done!"
	gtk.main_quit()
	return

k = threading.Thread(target=watchwpa)
k.start()

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
watchwpa.n = n
n.set_from_file("/usr/share/pixmaps/gwibber.svg")
n.set_tooltip_text("Egg-Wireless")

gtk.main()
