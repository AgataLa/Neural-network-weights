from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QFrame, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import pyqtSignal
import math
import torch
from moneyDetection import CaptureThread

WIDTH = 1000
HEIGHT = 700
IS_LIVE = False

colors = {"1gr" : '#92CC17', "2gr" : '#520085', "5gr" : '#92CC17', "10gr" : '#FF701F',
            "20gr" : '#344593', "50gr" : '#FF701F', "1zl" : '#1A9334', "2zl" : '#FF95C8',
            "5zl" : '#1A9334', "10zl" : '#CFD231', "20zl" : '#0018EC', "50zl" : '#CFD231',
            "100zl" : '#FF3838', "200zl" : '#2C99A8', "500zl" : '#FF3838'}


class MoneyCountView(QGridLayout):
    capture_thread = None
    camera_frame = None
    recognized_frame = None
    sum_label = None
    model = None
    s_key_pressed_signal = pyqtSignal()
    finish_detection_signal = pyqtSignal()
    is_stopped = False

    def __init__(self, return_button):
        super().__init__()

        self.model = torch.load("resources/snn.pth", map_location='cpu')
        self.model.conf = 0.75
        self.model.eval()

        self.setHorizontalSpacing(40)
        self.setVerticalSpacing(0)

        self.camera_frame = CameraFrame()
        self.addWidget(self.camera_frame, 1, 0, 1, 3, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.recognized_frame = RecognizedFrame()
        self.addWidget(self.recognized_frame, 2, 0, 1, 2, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        rec_title = MoneyCountTitle(self.recognized_frame, "Rozpoznano")
        rec_title.setGeometry(15, 10, 300, 50)

        sum_frame = SumFrame()
        self.addWidget(sum_frame, 2, 2, 1, 1, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        sum_title = MoneyCountTitle(sum_frame, "Suma:")
        sum_title.setGeometry(25, 10, 300, 50)


        self.sum_label = SumLabel(sum_frame)
        self.sum_label.setGeometry(0, 75, 275, 80)

        self.addWidget(return_button, 0, 0)
        
    
    def on_key_s_pressed(self):
        self.is_stopped = not self.is_stopped
        self.s_key_pressed_signal.emit()

    def on_camera_not_found(self):
        self.camera_frame.set_text("Nie można połączyć się z kamerą")

    def on_detection_completed(self, content):
        if not self.is_stopped:
            if not content["coins"] == None:
                self.recognized_frame.update_labels(content["coins"])
            if not content["sum"] == None:
                self.sum_label.setText("%.2f zł" % content["sum"])
            if not content["img"] == None:
                self.camera_frame.set_pixmap(content["img"])

    def on_detection_completed_s(self, content):
        if not content["coins"] == None:
            self.recognized_frame.update_labels(content["coins"])
        if not content["sum"] == None:
            self.sum_label.setText("%.2f zł" % content["sum"])
        if not content["img"] == None:
            self.camera_frame.set_pixmap(content["img"])

    def start_detection(self):
        self.capture_thread = CaptureThread(self.model)
        self.is_stopped = False

        self.capture_thread.start()
        self.capture_thread.camera_not_found_signal.connect(self.on_camera_not_found)
        self.capture_thread.detection_completed.connect(self.on_detection_completed)
        self.capture_thread.detection_completed_s.connect(self.on_detection_completed_s)
        self.s_key_pressed_signal.connect(self.capture_thread.on_s_key_pressed)
        self.finish_detection_signal.connect(self.capture_thread.on_finish_detection)

        button_live = LiveButton(self.capture_thread)
        self.addWidget(button_live, 0, 2, alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

    def finish_detection(self):
        self.finish_detection_signal.emit()
        



class RecognizedBox(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(20,70,0,0)
        self.setSpacing(0)
        self.setHorizontalSpacing(10)
        self.setVerticalSpacing(0)

        vbox0 = QVBoxLayout()
        vbox0.setSpacing(0)
        self.addLayout(vbox0, 0, 0, alignment=QtCore.Qt.AlignLeft)
        vbox1 = QVBoxLayout()
        vbox1.setSpacing(0)
        self.addLayout(vbox1, 0, 1, alignment=QtCore.Qt.AlignLeft)
        vbox2 = QVBoxLayout()
        vbox2.setSpacing(0)
        self.addLayout(vbox2, 0, 2, alignment=QtCore.Qt.AlignLeft)
        vbox3 = QVBoxLayout()
        vbox3.setSpacing(0)
        self.addLayout(vbox3, 0, 3, alignment=QtCore.Qt.AlignLeft)
        vbox4 = QVBoxLayout()
        vbox4.setSpacing(0)
        self.addLayout(vbox4, 0, 4, alignment=QtCore.Qt.AlignLeft)

        for i in range(15):
            self.itemAt(math.floor(i / 3)).layout().addWidget(MoneyLabel())

    def update_labels(self, coins):
        for i in range(15):
            self.itemAt(math.floor(i / 3)).layout().itemAt(i % 3).widget().setText("")
        for pos, key in enumerate(coins):
            name = key.split("_")[0]
            self.itemAt(math.floor(pos / 3)).layout().itemAt(pos % 3).widget().setText(name + " x " + str(coins[key]))
            self.itemAt(math.floor(pos / 3)).layout().itemAt(pos % 3).widget().setStyleSheet(MoneyLabel.styleSheet + "color: " + colors[name] + ";")



class MoneyLabel(QLabel):
    styleSheet = '''
        font-size: 22px;
        font-weight: bold;
        border: none;
        background: transparent;
        margin: 0px;
        margin-right: 10px;
        padding: 0px;
       '''

    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setStyleSheet(self.styleSheet)

class SumLabel(QLabel):
    def __init__(self, frame):
        super().__init__(frame)
        self.setText("0 zł")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet(
        '''
            font-size: 50px;
            font-weight: bold;
            border: none;
            background: transparent;
        '''
        )

class RecognizedFrame(QFrame):
    rec_grid = None
    def __init__(self):
        super().__init__()
        self.setFixedHeight(200)
        self.setFixedWidth(600)
        self.setStyleSheet(
        '''
                border: 3px solid black;
                background: '#1C1C1C';
                border-radius: 30px;
                font-size: 25px;
                margin-left: 60px;
                color: 'white';
            '''
        )
        self.rec_grid = RecognizedBox()
        self.setLayout(self.rec_grid)

    def update_labels(self, coins):
        self.rec_grid.update_labels(coins)

class CameraFrame(QFrame):

    camera = None

    def __init__(self):
        super().__init__()
        self.camera = QLabel(self)
        self.camera.setFixedHeight(350)
        self.camera.setFixedWidth(800)
        self.camera.setAlignment(QtCore.Qt.AlignCenter)
        self.camera.setStyleSheet(
                '''
                    font-size: 34px;
                    font-weight: bold;
                    border: none;
                    border-radius: 30px;
                    background: transparent;
                '''
                )
        self.camera.setGeometry(25, 25, 300, 50)

        self.setFixedHeight(400)
        self.setFixedWidth(WIDTH - 150)
        self.setStyleSheet(
        '''
                border: 3px solid black;
                background: '#1C1C1C';
                border-radius: 30px;
                font-size: 25px;
                color: 'white';
            '''
        )

    def set_text(self, content):
        self.camera.setStyleSheet('''
            color: '#730707';
            font-size: 36px;
            border: none;
            font-weight: bold;
            ''')
        self.camera.setText(content)

    def set_pixmap(self, content):
        self.camera.setPixmap(content)
        

class MoneyCountTitle(QLabel):
    def __init__(self, frame, text):
        super().__init__(frame)
        self.setText(text)
        self.setStyleSheet(
        '''
            font-size: 34px;
            font-weight: bold;
            border: none;
            background: transparent;
        '''
        )
        
class LiveButton(QPushButton):
    is_live_pressed = pyqtSignal(bool)

    def __init__(self, thread):
        super().__init__("  LIVE")
        self.setCheckable(True)
        self.setMinimumWidth(140)
        self.setMaximumWidth(140)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.setStyleSheet(
        '''
            *{border: 3px solid black;
            background: '#1C1C1C';
            border-radius: 20px;
            font-size: 25px;
            color: 'white';}
            *:hover{
                background: '#404040';
            }
            *:checked{
                background: '#fcba03';
            }
        '''
        )
        self.setIcon(QIcon("resources/live.png"))
        self.setIconSize(QtCore.QSize(35, 25))
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.clicked.connect(self.set_live)

        self.is_live_pressed.connect(thread.set_is_live)

    def set_live(self):
        self.is_live_pressed.emit(self.isChecked())

class SumFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(200)
        self.setFixedWidth(275)
        self.setStyleSheet(
        '''
                border: 3px solid black;
                background: '#1C1C1C';
                border-radius: 30px;
                font-size: 25px;
                color: 'white';
            '''
        )