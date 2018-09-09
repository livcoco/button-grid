#!/usr/bin/env python
# Re: Make a grid of message buttons
# - jiw -  1 Sept 2018

# 2nd qt5 version of boxgrid; builds CSS code based on specs in XML
# file, instead of coding it inline.  Refs grid2.xml, not grid1.xml

import sys
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QWidget, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from re import search
from macroSubst import macroSubst
from xml.etree import ElementTree

class xybutton(QPushButton):
    perx, pery = 42, 42         # Grid cell side lengths
    bux,  buy  = 40, 40         # Button side lengths
    def __init__(self, labl='B', par=None, codename='cat0', x=0, y=0, dat='t'):
        # Init super fields and link to parent widget
        super(QPushButton, self).__init__(parent=par)
        self.setObjectName(codename) # Set kind of style to use
        self.setText(labl)           # Set button's label
        self.clicked.connect(xyBcallback) # Callback handler
        self.setMinimumSize(self.bux, self.buy)   # Button min size
        self.move(x*self.perx, y*self.pery) # Button location
        self.x, self.y, self.dat = x, y, dat

def xyBcallback():      # xyButton callback handler
    me = W.sender()     # ! W is a global ref to widget level above us
    nam, cat, dat, x, y = me.text(), me.objectName(), me.dat, me.x, me.y
    print ('{:>10} {:>10} {:>10} x{:<2} y{:<2}'.format(nam, cat, dat, x, y))

def ErrorExit(msg, fname):
    sys.stderr.write('\n*** {} {} ***\n'.format(msg, fname))
    sys.exit(0)

def makeGrid(etree):
    at = ''                     # set default for at
    recot = {}
    recon = {}
    for item in etree.getroot():
        if shoInput>1:
            print (item.tag, item.attrib, len(item), item.keys())
	if item.tag == 'deco':
            pass        # future: frame/ontop/stick
        elif item.tag=='macro':
            for k in item.keys():
                recot[k] = macroSubst(item.get(k), recot, recon)
                s = search(r' *(\d+)', recot[k])                
                recon[k] = int(s.expand(r'\1')) if s else 0
                if shoInput>0:
                    print ('macro {}: {}  {}'.format(k, recot[k], recon[k]))
        elif item.tag=='style':
            pass        # future:
        elif item.tag=='item':
            clv = dict(item.items())
            for term in clv.keys():
                toft = clv[term] # Get text of term
                clv[term] = macroSubst(toft, recot, recon)
            if shoInput>0:
                print ('{} {}'.format(item.tag, clv.items()))
            # Make button with labl l, codename c, data v.
            l = clv.get('l', '?')
            B = xybutton(l, W, clv['i'], int(clv['c']), int(clv['r']), clv['v'])

# --------------------------- main -------------------------------
# Get params: (1) output-options number, (2) name of grid XML file
shoInput = int(sys.argv[1]) if len(sys.argv) > 1  else 0
gridFile = sys.argv[2]      if len(sys.argv) > 2  else './grid2.xml'

try:                            # Read script from file and parse it
    etree = ElementTree.parse(gridFile)
except IOError:
    ErrorExit('IOError, check file or filename', gridFile)
except ElementTree.ParseError:
    ErrorExit('ParseError, check XML validity in file', gridFile)
except:                         # Some unknown error
    ErrorExit('Error while treating', gridFile)

# Build boxgrid data structure and its display window
app = QApplication(['hey'])
W = QWidget()
W.setWindowTitle('qt-color-try')
hix, hiy = 4, 15                # !! Should get hix, hiy from XML data
wide, high = hix*xybutton.perx, hiy*xybutton.pery
W.setMinimumSize(wide, high)
atx, aty = 1060, 380
W.move(atx, aty)
# Set main window background color etc
W.setStyleSheet("""
QWidget { background-color: coral;
}
QPushButton {
  color: blue; font: bold 11px; padding: 1;  border: 1 solid lawngreen;
  background-color: lawngreen;
}
QPushButton#cat0         { color: violet; background-color: darkgreen; }
QPushButton#cat0:pressed { color: red;    background-color: Aquamarine; }

QPushButton#cat1         { color: white;  background-color: Chocolate;}
QPushButton#cat1:pressed { color: red;    background-color: Bisque; }

QPushButton#cat2         { color: pink;   background-color: darkblue; }
QPushButton#cat2:pressed { color: red;    background-color: cyan; }

QPushButton#cat3         { color: black;  background-color: crimson; }
QPushButton#cat3:pressed { color: black;  background-color: beige; }
""")

#W.override_background_color(Gtk.StateFlags.NORMAL, color)

makeGrid(etree)         # Make a button grid, using data from XML tree
W.show()                    # Show window
exit(app.exec_())           # run pyQt5 event loop until window closes