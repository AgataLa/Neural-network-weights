from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QStackedWidget
from PyQt5.QtGui import QIcon, QCursor
from mainMenuView import MainMenuView
from appInfoView import AppInfoView
from moneyCountView import MoneyCountView

class MainWindow(QMainWindow):
    WIDTH = 1000
    HEIGHT = 700
    bg_style = '''
        background: url(resources/background.jpeg);
        border: 2px solid black;
        '''
    widget = None
    money_count_view = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoneyCounter")
        self.setFixedWidth(self.WIDTH)
        self.setFixedHeight(self.HEIGHT)
        self.setStyleSheet(self.bg_style)

        self.widget = QStackedWidget()

        return_button_from_app_info = ReturnButton(self.go_to_main_menu_view)
        return_button_from_money_count = ReturnButton(self.go_to_main_menu_view_and_finish_detection)
    
        main_menu_view = MainMenuView(self.go_to_app_info_view, self.go_to_money_count_view)
        app_info_view = AppInfoView(return_button_from_app_info)
        self.money_count_view = MoneyCountView(return_button_from_money_count)

        main_menu = QWidget()
        main_menu.setLayout(main_menu_view)

        app_info = QWidget()
        app_info.setLayout(app_info_view)

        money_count = QWidget()
        money_count.setLayout(self.money_count_view)

        self.widget.addWidget(main_menu)
        self.widget.addWidget(app_info)
        self.widget.addWidget(money_count)
        
        self.setCentralWidget(self.widget)

    def go_to_app_info_view(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def go_to_main_menu_view(self):
        self.widget.setCurrentIndex(0)

    def go_to_main_menu_view_and_finish_detection(self):
        self.widget.setCurrentIndex(0)
        self.money_count_view.finish_detection()

    def go_to_money_count_view(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 2)
        self.money_count_view.start_detection()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_S:
            self.money_count_view.on_key_s_pressed()
        

class ReturnButton(QPushButton):

    def __init__(self, action):
        super().__init__()
        self.setMinimumWidth(90)
        self.setMaximumWidth(90)
        self.setMinimumHeight(60)
        self.setMaximumHeight(60)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
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
        '''
        )
        self.setIcon(QIcon("resources/arrow.png"))
        self.setIconSize(QtCore.QSize(45, 45))
        self.clicked.connect(action)
