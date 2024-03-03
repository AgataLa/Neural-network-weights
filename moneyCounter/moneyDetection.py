from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
import re
import cv2 as cv
import numpy as np
import time


class CaptureThread(QThread):
    width = 1024
    height = 450
    model = None
    is_live = False
    current_frame = None
    stopped = False
    running = True
    ready_img = None

    camera_not_found_signal = pyqtSignal()
    detection_completed = pyqtSignal(dict)
    detection_completed_s = pyqtSignal(dict)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        self.running = True
        self.is_live = False
        self.stopped = False

        cap = cv.VideoCapture("https://192.168.1.13:8080/video")

        if not cap.isOpened():
            self.camera_not_found_signal.emit()
            return

        cap.set(3, self.width)
        cap.set(4, self.height)
        cap.set(cv.CAP_PROP_FPS, 30)

        frame_rate = 2
        prev = 0

        while self.running:
            ret, self.current_frame = cap.read()

            while self.stopped and self.running:
                time.sleep(1)
                prev = time.time()
                continue
            while cap.isOpened() and self.running and not self.stopped:
                time_elapsed = time.time() - prev
                ret, self.current_frame = cap.read()
                if self.is_live and time_elapsed < 1./frame_rate:
                    continue
                prev = time.time()
                if self.current_frame is None:
                    continue
                img = prepare_img(self.current_frame)

                result_dict = {"sum": None, "coins": None, "img": None}

                if self.is_live:
                    coins_sum, coins = self.recognize_and_sum_coins(img)
                    result_dict["sum"] = coins_sum
                    result_dict["coins"] = coins

                self.ready_img = create_pixmap(img)

                if not self.stopped:
                    result_dict["img"] = self.ready_img
                    self.detection_completed.emit(result_dict)

        cap.release()

    def set_is_live(self, is_live):
        self.is_live = is_live

    def on_s_key_pressed(self):
        if self.stopped == False:
            self.stopped = True
            self.perform_detection()
        else:
            self.stopped = False

    def on_finish_detection(self):
        self.running = False

    def recognize_and_sum_coins(self, img):
        result = self.model(img)
        img = np.squeeze(result.render())
        coins_sum, coins = sum_recognized_money(result.pandas().xyxy[0]['name'])
        return coins_sum, coins

    def perform_detection(self):
        result_dict = {"sum": None, "coins": None, "img": None}

        img = prepare_img(self.current_frame)
        coins_sum, coins = self.recognize_and_sum_coins(img)
    
        result_dict["sum"] = coins_sum
        result_dict["coins"] = coins
        self.ready_img = create_pixmap(img)
        result_dict["img"] = self.ready_img
        self.detection_completed_s.emit(result_dict)


def create_pixmap(img):
    img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
    pix = QPixmap.fromImage(img)
    pix = pix.scaled(800, 350, Qt.KeepAspectRatio)
    return pix


def sum_recognized_money(money_names):
    image_sum = 0.0
    recognized = {}
    for value in money_names:
        if value.split("_")[0] in recognized:
            recognized[value.split("_")[0]] += 1
        else:
            recognized[value.split("_")[0]] = 1

        if bool(re.match(r"\d+zl*", value)):
            image_sum += int(value.split("z")[0])
        elif bool(re.match(r"\d+gr*", value)):
            image_sum += float(value.split("g")[0])/100

    return image_sum, recognized

def prepare_img(frame):
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    return img