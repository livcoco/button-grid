#!/usr/bin/env python
# Re: Make a grid of message buttons
# - jiw -  1 Sept 2018

# 2nd qt5 version of boxgrid; builds CSS code based on specs in XML
# file, instead of coding it inline.  Refs grid2.xml, not grid1.xml

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout
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
        self.move(x*self.perx, y*self.pery) # Button location
        self.x, self.y, self.dat = x, y, dat
                
def xyBcallback():      # xyButton callback handler
    me = W.sender()     # ! W is a global ref to widget level above us
    nam, cat, dat, x, y = me.text(), me.objectName(), me.dat, me.x, me.y
    print ('{:>10} {:>10} {:>10} x{:<2} y{:<2}'.format(nam, cat, dat, x, y))

def ErrorExit(msg, fname):
    sys.stderr.write('\n*** {} {} ***\n'.format(msg, fname))
    sys.exit(0)

def formStyle(widg, name, state, props, sociate):
    styl = widg + ('#'+name if name else '') + state + ' {'
    for key in sociate.keys():
        if key in props:        # Make an l:v style item
            l = sociate[key]    # eg background-color
            v = props[key]      # eg green
            if l:     # Add (eg) `background-color: "Bisque";` to body
                styl += ' {}: "{}"; '.format(sociate[key], v)
            elif key=='vc' or key=='vp':
                styl += v
    return styl + ' }'

def makeGrid(etree, W, L):
    at = ''                     # set default for at
    recot = {}
    recon = {}
    styleBlob = ''              # To build style-sheet text
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
        elif item.tag=='item' or item.tag=='style':
            props = dict(item.items())
            for term in props.keys():
                toft = props[term] # Get text of term
                props[term] = macroSubst(toft, recot, recon)
            if shoInput>0:
                print ('{} {}'.format(item.tag, props.items()))
            # Prepare associations for arbitrary and not-pressed widget styles
            sociate = { 'tc':'color', 'bc':'background-color', 'vc':'', 'mh':'min-height', 'mw':'min-width' }
            objCode = props.get('obj','')
            objName = props.get('id','')
            # Now make a button or style with given properties
            if item.tag=='item': # Button with labl l, codename c, data v.
                l = props.get('l', '?')
                B = xybutton(l, W, props['i'], int(props['c']), int(props['r']), props['v'])
                L.addWidget(B, B.y, B.x)
            # Styles with id, tc, bc, vc, mh, mw, tp, bp, vp
            elif objCode:    # Generate framework for arbitrary widget
                fs = formStyle(objCode, objName, '', props, sociate)
                styleBlob += fs
                if shoInput>0:
                    print ('formStyle: {}'.format(fs))
                if shoInput>1:
                    print ('styleBlob: {}'.format(styleBlob))
            else: # Generate QPushButton and QPushButton:pressed frameworks
                for state in ('', ':pressed'):
                    fs = formStyle('QPushButton', objName, state, props, sociate)
                    styleBlob += fs
                    if shoInput>0:
                        print ('formStyle: {}'.format(fs))
                    if shoInput>1:
                        print ('styleBlob: {}'.format(styleBlob))
                    sociate = { 'tp':'color', 'bp':'background-color', 'vp':'' }
    W.setStyleSheet(styleBlob)
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
L = QGridLayout()
W.setLayout(L)                  # Add layout manager to window
W.setWindowTitle('qt-color-try')
atx, aty = 1060, 380
W.move(atx, aty)
#W.override_background_color(Gtk.StateFlags.NORMAL, color)
makeGrid(etree, W, L)   # Make a button grid, using data from XML tree
W.show()                    # Show window
exit(app.exec_())           # run pyQt5 event loop until window closes
