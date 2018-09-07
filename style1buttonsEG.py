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
            color: red;
            background-color: palegreen;
} """)

        # Create button
        btn1 = QPushButton('Click Me')
        btn1.setProperty('Rank', 1)
        btn1.setObjectName('StyledButton')
        btn1.clicked.connect(lambda: self.toggle(btn1))
        layout.addWidget(btn1)

    def toggle(self, widget):
        # Query the attribute
        isTest = widget.property('Test') #.toBool()
        widget.setProperty('Test', not isTest)

        # Update the style
        widget.setStyle(widget.style())

if __name__ == '__main__':
    app = QApplication([])
    dlg = Test()
    dlg.show()
    app.exec_()
