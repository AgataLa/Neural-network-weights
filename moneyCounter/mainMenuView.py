from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor

class MainMenuView(QGridLayout):

    def __init__(self, go_to_app_info, go_to_money_count_view):
        super().__init__()

        self.setSpacing(50)
        self.__create_logo()
        self.__create_buttons(go_to_app_info, go_to_money_count_view)

    def __create_logo(self):
        image = QPixmap("resources/logo.png")
        logo = QLabel()
        logo.setPixmap(image)
        logo.setStyleSheet(
        '''
            background: transparent;
            border: none;
            margin-top: 80px;
        '''
            )
        self.addWidget(logo, 0, 0, 2, 2, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

    def __create_buttons(self, go_to_app_info, go_to_money_count_view):
        button_start = MainMenuButton("Oblicz kwotę", go_to_money_count_view)
        button_info = MainMenuButton("O aplikacji", go_to_app_info)

        self.addWidget(button_start, 3, 0, 1, 2, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.addWidget(button_info, 4, 0, 2, 2, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)


class MainMenuButton(QPushButton):

    def __init__(self, text, action):
        super().__init__(text)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setMinimumWidth(300)
        self.setMinimumHeight(70)
        self.setStyleSheet(
            '''
                *{border: 3px solid black;
                background: '#1C1C1C';
                border-radius: 30px;
                font-size: 25px;
                font-weight: bold;
                color: 'white';}
                *:hover{
                    background: '#404040';
                }
            '''
            )
        self.clicked.connect(action)