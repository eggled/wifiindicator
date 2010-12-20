#!/usr/bin/env python
import gtk,time

n = gtk.StatusIcon()
n.set_from_file("/usr/share/pixmaps/gwibber.svg")
n.set_tooltip_text("Egg-Wireless")

gtk.main()
