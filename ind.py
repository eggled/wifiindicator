#!/usr/bin/env python
import gtk,time,threading

def watchwpa():
	print "Doing my sleeping"
	time.sleep(5)
	print "All done!"
	return

k = threading.Thread(target=watchwpa)
k.start()

gtk.gdk.threads_init()
n = gtk.StatusIcon()
n.set_from_file("/usr/share/pixmaps/gwibber.svg")
n.set_tooltip_text("Egg-Wireless")

gtk.main()
