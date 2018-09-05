#!/usr/bin/env python
# Re: Make a grid of message buttons
# -- attempt to color buttons individually
# - jiw -  2 Sept 2018

import gi
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
    perx, pery = 50, 40
    
    def __init__(self, labl='B', par=None, x=0, y=0, t='t'):
        super(QPushButton, self).__init__(parent=par)
        self.setText(labl)
        self.clicked.connect(bgBC)
        self.resize(self.perx, self.pery)
        self.move(x*self.perx, y*self.pery)
        self.x, self.y, self.txt = x, y, t

    def colorStyle(borderCol, backCol):
        self.setStyleSheet('xybutton { border: 12px {};  background-color: {} }'.format(borderCol, backCol))

app = QApplication(['hey'])
W = QWidget()
W.setWindowTitle('qt-color-try')
palette = W.palette()
role = W.backgroundRole() # for background color
palette.setColor(role, QColor('green'))
W.setPalette(palette)
W.setAutoFillBackground(True)

hix, hiy = 7, 11
wide, high = hix*xybutton.perx, hiy*xybutton.pery
atx, aty = 1060, 380
W.resize(wide, high)
W.move(atx, aty)

for k in range(17):
    x, y, l = randint(0,hix-1), randint(0,hiy-1), 'B{}'.format(k)
    B = xybutton(l, W, x, y, l)
    palette = B.palette()
    role = B.backgroundRole()
    palette.setColor(role, QColor(colors[randint(0,len(colors)-1)]))
    B.setPalette(palette)
    B.setAutoFillBackground(True)
    print ('Placed button {} at {},{} : {}'.format(k, x, y, B.txt))

W.show()                        # Show the widget
exit(app.exec_())               # Run the event loop until window closes
