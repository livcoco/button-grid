#!/usr/bin/env python
# Re: Make a grid of message buttons
# -- attempt to color buttons individually
# - jiw -  2 Sept 2018

#import gi
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from random import randint
from time import sleep
from sys import exit

colors = ('red', 'pink', 'cyan', 'blue', 'green', 'white')

def bgBC():  # bgBC: boxgrid Button Callback handler
    sender = W.sender()
    print ('bgBC: txt@x,y = {}@{},{}'.format(sender.txt,sender.x,sender.y))
   
class xybutton(QPushButton):
    perx, pery = 45, 45
    
    def __init__(self, labl='B', par=None, x=0, y=0, t='t'):
        super(QPushButton, self).__init__(parent=par)
        self.setText(labl)
        self.clicked.connect(bgBC)
        self.resize(self.perx, self.pery)
        self.move(x*self.perx, y*self.pery)
        self.x, self.y, self.txt = x, y, t

#    def colorStyle(self, borderCol, backCol):
        #self.setStyleSheet('QPushButton#xybutton \{ border: 12px {};  background-color: {} \}'.format(borderCol, backCol))
#        self.setStyleSheet('QPushButton#xybutton { border: 12px red;  background-color: green }')

app = QApplication(['hey'])
W = QWidget()
W.setWindowTitle('qt-color-try')

hix, hiy = 7, 11
wide, high = hix*xybutton.perx, hiy*xybutton.pery
atx, aty = 1060, 380
W.resize(wide, high)
W.move(atx, aty)
#W.setStyleSheet('QPushButton#xybutton { border: 12px red;  background-color: green }')
palette = W.palette()
role = W.backgroundRole() # for background color
palette.setColor(role, QColor('green'))
W.setPalette(palette)

for k in range(17):
    x, y, l = randint(0,hix-1), randint(0,hiy-1), 'B{}'.format(k)
    B = xybutton(l, W, x, y, l)
    cbord = cback = colors[randint(0,len(colors)-1)]
    while cbord==cback:
        cback = colors[randint(0,len(colors)-1)]
    #B.colorStyle(QColor(cbord), QColor(cback))
    role = B.backgroundRole() # for background color
    palette = B.palette()
    palette.setColor(role, QColor(cback))
    B.setPalette(palette)
    print ('Placed button {:2} at {:2},{:<2} with colors {:>5}, {}'.format(k, x, y, cbord, cback))

W.show()                        # Show the widget
exit(app.exec_())               # Run the event loop until window closes
