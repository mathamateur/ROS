from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QImage, QPalette, QBrush
import sys


class Interface(QWidget):
    def __init__(self):
        super().__init__()
        
        #play and beat buttons
        self.play_button = QPushButton(self)
        self.play_button.setText("Play")
        self.play_button.setFont(QFont('Comic Sans MS', 15))
        self.play_button.resize(100, 50)
        
        self.beat_button = QPushButton(self)
        self.beat_button.setText("Beat")
        self.beat_button.setFont(QFont('Comic Sans MS', 15))
        self.beat_button.resize(100, 50)
        
        self.buttons_hbox = QHBoxLayout()
        self.buttons_hbox.addWidget(self.beat_button, 0, Qt.AlignLeft)
        self.buttons_hbox.addWidget(self.play_button, 0, Qt.AlignRight)
        
        #label Make your melody
        self.ins_label = QLabel()
        self.ins_label.setText("Make your melody")
        self.ins_label.setFont(QFont('Comic Sans MS', 30))
        self.ins_label.setStyleSheet('color: white')
        self.ins_label.setAlignment(Qt.AlignCenter)
        
        #check-boxes
        self.drums_cb = QCheckBox()
        self.drums_cb.setText("Drums")
        self.drums_cb.setFont(QFont('Comic Sans MS', 20))
        
        self.hihat_cb = QCheckBox()
        self.hihat_cb.setText("Hi-Hat")
        self.hihat_cb.setFont(QFont('Comic Sans MS', 20))
        
        self.bass_cb = QCheckBox()
        self.bass_cb.setText("Bass")
        self.bass_cb.setFont(QFont('Comic Sans MS', 20))
        
        self.cbs_hbox = QHBoxLayout()
        self.cbs_hbox.addWidget(self.drums_cb, 0, Qt.AlignLeft)
        self.cbs_hbox.addWidget(self.hihat_cb, 0, Qt.AlignCenter)
        self.cbs_hbox.addWidget(self.bass_cb, 0, Qt.AlignRight)
        
        #harmonic canvas button
        self.harm_button = QPushButton(self)
        self.harm_button.setText("Show harmonic canvas")
        self.harm_button.setFont(QFont('Comic Sans MS', 15))
        self.harm_button.resize(200, 50)
        self.harm_button.clicked.connect(self.harm)
        
        #Main widget
        self.main_vbox = QVBoxLayout()
        self.main_vbox.addLayout(self.buttons_hbox)
        self.main_vbox.addWidget(self.ins_label)
        self.main_vbox.addLayout(self.cbs_hbox)
        self.main_vbox.addWidget(self.harm_button, 0, Qt.AlignCenter)
        self.main_vbox.setContentsMargins(100, 50, 100, 50)
        
        #Main window settings
        self.setLayout(self.main_vbox)
        self.resize(700, 500)
        self.setWindowTitle('EyE_BeaT')
        oImage = QImage("ProektSPO/images/background.jpg")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))                        
        self.setPalette(palette)
        self.center()
        self.show()
        
        
    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        
    def harm(self):
        self.close()
    
    
app = QApplication(sys.argv)        
app.lastWindowClosed.connect(quit)
w = Interface()
app.exec_()
import Trecker_with6acord




