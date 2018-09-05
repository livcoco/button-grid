#!/usr/bin/env python
# Re: Make a grid of message buttons
# - jiw -  1 Sept 2018

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from re import sub, search
from xml.etree import ElementTree

def ErrorExit(msg, fname):
    sys.stderr.write('\n*** {} {} ***\n'.format(msg, fname))
    sys.exit(0)

def bgBC(widget, val):  # bgBC: boxgrid Button Callback handler
    print 'bgBC: ', val

def makeGrid(etree):
    at = ''                     # set default for at
    recot = {}
    recon = {}
    row = 0
    grid = Gtk.Grid()
    W.add(grid)
    #bu = Gtk.Button()
    #buCoMap = bu.gdk.get_colormap()
    #buStyle = bu.get_style().copy()
    for item in etree.getroot():
        print item.tag, item.attrib, len(item)
	if item.tag == 'info':
            for elt in item:
                print elt.tag,elt.items()
                if elt.tag=='deco':
                    pass        # future: frame/ontop/stick
                if elt.tag=='code':
                    for k in elt.keys():
                        recot[k] = elt.get(k)
                        recon[k] = 0
        elif item.tag=='row':
            col = 0
            RBox = Gtk.HBox()
            for elt in item:
                clv = dict(elt.items())
                for term in clv.keys():
                    toft = clv[term] # Get text of term
                    if toft[0]=='%':  # Is toft a macro?
                        mname = toft[1:]     # Yes, get its name
                        mbody = recot[mname] # Get body of macro
                        s = mbody.find('%#')  # Is a # in macro?
                        if s > -1:
                            mbody = sub('%#', str(recon[mname]), mbody)
                            recon[mname] += 1  # Increase counter
                        clv[term] = mbody
                print '{} {}'.format(elt.tag, clv.items())
                B  = Gtk.Button(label=clv.get('l','-')); # make a button
                B.connect('clicked', bgBC, clv.get('v',str(100*row+col)))
                #buStyle.bg[Gtk.STATE_NORMAL] = buCoMap.alloc_color(clv.get('c','black'))
                #B.set_style(buStyle)           # Set the button color
                #color = Gdk.color_parse(clv.get('c','black'))
                #B.modify_bg(Gtk.StateFlags.ACTIVE, color)
                #B.modify_bg(Gtk.StateFlags.NORMAL, color)
                #B.modify_bg(Gtk.StateFlags.PRELIGHT, color)
                #B.modify_bg(Gtk.StateFlags.SELECTED, color)
                #B.modify_bg(Gtk.StateFlags.INSENSITIVE, color)
                #B.modify_bg(Gtk.StateFlags.FOCUSED, color)
                #B.modify_bg(Gtk.StateFlags., color)
                color=Gdk.RGBA()
                color.parse(clv.get('c','black'))
                color.to_string()
                B.override_background_color(Gtk.StateFlags.NORMAL, color)
                #B.override_background_color(Gtk.StateFlags.ACTIVE, color)
                #B.override_background_color(Gtk.StateFlags.NORMAL, color)
                #B.override_background_color(Gtk.StateFlags.PRELIGHT, color)
                #B.override_background_color(Gtk.StateFlags.SELECTED, color)
                #B.override_background_color(Gtk.StateFlags.FOCUSED, color)
                grid.attach(B, col, row, 1, 1) # add button to grid
                col += 1
            row += 1

# Read a script and build menu window structures
gridFile = './grid1.xml' if len(sys.argv)<2 else sys.argv[1]

try:
    etree = ElementTree.parse(gridFile)
except IOError:
    ErrorExit('IOError, check file or filename', gridFile)
except ElementTree.ParseError:
    ErrorExit('ParseError, check XML validity in file', gridFile)
except:
    ErrorExit('Error while treating', gridFile)

# Build boxgrid data structure and its display window
W = Gtk.Window()
W.connect('destroy', Gtk.main_quit) # Set up 'x' action
makeGrid(etree)

# Handle events
W.show_all()
Gtk.main() # run pygtk event loop
