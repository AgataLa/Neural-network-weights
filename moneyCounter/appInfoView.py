from PyQt5.QtWidgets import QLabel, QGridLayout, QFrame
from PyQt5 import QtCore

WIDTH = 1000
HEIGHT = 700

class AppInfoView(QGridLayout):

    def __init__(self, return_button):
        super().__init__()

        self.setHorizontalSpacing(0)
        self.setVerticalSpacing(0)
        self.addWidget(return_button, 0, 0)
        self.__create_info_box()
    

    def __create_info_box(self):
        info_box = QFrame()
        info_box.setFixedHeight(HEIGHT - 150)
        info_box.setFixedWidth(WIDTH - 150)
        info_box.setStyleSheet(
            '''
                border: 3px solid black;
                background: '#1C1C1C';
                border-radius: 30px;
                font-size: 25px;
                color: 'white';
            '''
        )

        self.__create_section_titles(info_box)
        self.__create_section_texts(info_box)

        self.addWidget(info_box, 1, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)


    def __create_section_titles(self, info_box):
        general_title = AppInfoSectionTitle(info_box, "O aplikacji")
        usage_title = AppInfoSectionTitle(info_box, "Jak korzystać z aplikacji?")
        general_title.setGeometry(35, 25, 300, 50)
        usage_title.setGeometry(35, 300, 600, 50)

    def __create_section_texts(self, info_box):
        app_general_info = AppInfoSectionText(info_box, app_general_info_text)
        app_general_info.setGeometry(35, 25, WIDTH - 150 - 70, 300)
        app_usage_info = AppInfoSectionText(info_box, app_usage_info_text)
        app_usage_info.setGeometry(35, 290, WIDTH - 150 - 70, 300)


class AppInfoSectionTitle(QLabel):

    def __init__(self, box, text):
        super().__init__(box)
        self.setText(text)
        self.setStyleSheet(
            '''
            font-size: 34px;
            font-weight: bold;
            border: none;
            background: transparent;
        '''
        )


class AppInfoSectionText(QLabel):
    def __init__(self, box, text):
        super().__init__(box)
        self.setWordWrap(True)
        self.setText(text)
        self.setStyleSheet(
            '''
            font-size: 18px;
            border: none;
            font-weight: medium;
            background: transparent;
        '''
        )


app_general_info_text = "Aplikacja MoneyCounter służy do obliczania kwoty pieniędzy widocznych na obrazie z kamery."\
    "\nW celu identyfikacji odpowiednich monet i banknotów zastosowana została sieć neuronowa YOLOv5.\n\n"\
    "Aby móc korzystać z aplikacji niezbędne jest posiadanie dostępnej na komputerze kamerki."

app_usage_info_text = "W celu obliczenia kwoty pieniędzy wystarczy wybrać opcję “Oblicz kwotę”,\n"\
    "a następnie nakierować kamerkę na pieniądze, które mają zostać zsumowane\ni nacisnąć przycisk \"s\".\n"\
    "Dostępne są dwa tryby detekcji pieniędzy – \"LIVE\" lub po naciśnięciu przycisku \"s\" (domyślny). "\
    "Tryb \"LIVE\" umożliwia obliczanie kwoty na bieżąco z obrazu z kamery. Aby go uruchomić należy wcisnąć przycisk \"LIVE\" znajdujący się u góry ekranu."
