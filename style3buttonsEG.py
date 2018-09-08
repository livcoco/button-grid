#!/usr/bin/env python
# Re:  attempt to format buttons individually
# - jiw -  6 Sept 2018
# Ref: http://dgovil.com/blog/2017/02/24/qt_stylesheets/

from PyQt5.QtWidgets import QVBoxLayout, QDialog, QWidget, QPushButton, QApplication

class Test(QDialog):
    """A sample widget to show dynamic properties with stylesheets"""
    def __init__(self):
        super(Test, self).__init__()
        self.setWindowTitle('Style Sheet Test')
        layout = QVBoxLayout(self)

        # Set the stylesheet
        # Property     Use
        #   color    text color
        #   font     font options, eg bold or size or family
        #   border   width & color of border around content
        #   background-color   background color of content area
        #   padding: 2px;
        #   border-style: inset/outset;
        self.setStyleSheet("""
        QPushButton {
         color: blue;   font: bold 49px;
         padding: 17px;  border: 29px solid lawngreen;
         background-color: lawngreen;
        }
        QPushButton:pressed {
         color: violet;
         background-color: palegreen;
        }
        QPushButton#cat1:pressed {
         color: white;
         background-color: palegreen;
        }
        QPushButton#cat2:pressed {
         color: pink;
         background-color: palegreen;
        }
        QPushButton#cat3 {
         color: cyan;
         background-color: green;
        }
        QPushButton#cat3:pressed {
         color: cyan;
         background-color: peach;
        }
        """)

        b1 = self.makeButton('cat1', 'Click Me', 1, layout)
        b2 = self.makeButton('cat2', 'Not me!',  2, layout)
        b3 = self.makeButton('cat3', 'Etc etc',  3, layout)

    def makeButton(self, codename, txt, dat, lout):   # Create fine button
        B = QPushButton(txt)
        B.setProperty('Rank', dat)
        B.setObjectName(codename)
        B.clicked.connect(lambda: self.callback(B))
        lout.addWidget(B)

    def callback(self, widget):
        # Update the style
        #widget.setStyle(widget.style())
        # Tell about it
        print ('B r={} {}'.format(widget.property('Rank'),widget.text()))

if __name__ == '__main__':
    app = QApplication([])
    dlg = Test()
    dlg.show()
    app.exec_()
