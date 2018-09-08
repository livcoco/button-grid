#!/usr/bin/env python
# Re: Make a grid of message buttons
# - jiw -  1 Sept 2018

# Note, make a qt5 version of this, with CSS code built up based on
# colors etc specified in XML file.  The initial section of that file
# will define half a dozen or so button specs.  Each spec can include
# a button-type codename; text color and its font options (eg bold or
# size); and background color of content area when pressed and when
# not pressed.  Then in the <elt> entries allow l for label, c for
# button-type codename, and v for value to send.

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from re import sub, search
from xml.etree import ElementTree

def ErrorExit(msg, fname):
    sys.stderr.write('\n*** {} {} ***\n'.format(msg, fname))
    sys.exit(0)

def bgBC(widget, val, r, c):  # bgBC: boxgrid Button Callback handler
    print ('{:>10}   r{:<2} c{:<2}'.format(val, r, c))

def makeGrid(etree):
    at = ''                     # set default for at
    recot = {}
    recon = {}
    row = 0
    grid = Gtk.Grid()
    W.add(grid)
    for item in etree.getroot():
        if shoInput>0:
            print (item.tag, item.attrib, len(item))
	if item.tag == 'info':
            for elt in item:
                if shoInput>1:
                    print (elt.tag,elt.items())
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
                if shoInput>1:
                    print ('{} {}'.format(elt.tag, clv.items()))
                B  = Gtk.Button(label=clv.get('l','-')); # make a button
                B.connect('clicked', bgBC, clv.get('v',str(100*row+col)), row, col)
                grid.attach(B, col, row, 1, 1) # add button to grid
                col += 1
            row += 1

# Get params and read a script
shoInput = int(sys.argv[1]) if len(sys.argv) > 1  else 0
gridFile = sys.argv[2]      if len(sys.argv) > 2  else './grid1.xml'

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
color=Gdk.RGBA()                    # Get a white RGBA structure
color.parse('green')                # Change it to green
W.override_background_color(Gtk.StateFlags.NORMAL, color)
makeGrid(etree)

# Show window and handle events
W.show_all()
Gtk.main() # run pygtk event loop
