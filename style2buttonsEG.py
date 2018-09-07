#!/usr/bin/env python
# Re:  attempt to format buttons individually
# - jiw -  5 Sept 2018
# Ref: http://dgovil.com/blog/2017/02/24/qt_stylesheets/

from PyQt5.QtWidgets import QVBoxLayout, QDialog, QWidget, QPushButton, QApplication

class Test(QDialog):
    """A sample widget to show dynamic properties with stylesheets"""
    def __init__(self):
        super(Test, self).__init__()
        self.setWindowTitle('Style Sheet Test')
        layout = QVBoxLayout(self)

        # Set the stylesheet
        ##        border: 12px solid #8f8f91;
        self.setStyleSheet("""
            QPushButton {
                border: 8px solid pink;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 80px;
            }
            QPushButton[Rank=3] {
                border: 8px solid red;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 80px;
            }

            QPushButton#StyledButton[Rank=1] {
                border: 8px solid blue;
                color: #F00;
                background-color: #000;
            }

            QPushButton#StyledButton[Rank=2] {
                border: 8px solid purple;
                color: #F00;
                background-color: #000;
            }

            QPushButton#StyledButton[Rank=4] {
                border: 8px solid yellow;
            }

            QPushButton#StyledButton[Rank=5] {
                border: 8px solid green;
            }
                           """)

        # Create the button
        btn1 = QPushButton('Click Me')
        btn1.setProperty('Rank', 1)
        btn1.setObjectName('StyledButton')
        btn1.clicked.connect(lambda: self.toggle(btn1))
        layout.addWidget(btn1)

        btn2 = QPushButton('Click Me')
        btn2.setProperty('Rank', 2)
        btn2.clicked.connect(lambda: self.toggle(btn2))
        layout.addWidget(btn2)
        
        btn3 = QPushButton('Click Me')
        btn3.setProperty('Rank', 3)
        btn3.clicked.connect(lambda: self.toggle(btn3))
        layout.addWidget(btn3)
        
        btn4 = QPushButton('Click Me')
        btn4.setProperty('Rank', 4)
        btn4.clicked.connect(lambda: self.toggle(btn4))
        layout.addWidget(btn4)
        
        btn5 = QPushButton('Click Me')
        btn5.setProperty('Rank', 5)
        btn5.clicked.connect(lambda: self.toggle(btn5))
        layout.addWidget(btn5)

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
