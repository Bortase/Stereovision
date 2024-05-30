import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QPixmap, QImage  # Import QImage from QtGui
import cv2
import numpy as np
from ultralytics import YOLO

coordinates = []


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        self.model = YOLO(r'G:\stereovision\runs\detect\train2\weights\best.pt')
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.results = self.model(cv_img)

                for result in self.results:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    scores = result.boxes.conf.cpu().numpy()
                    classes = result.boxes.cls.cpu().numpy()

                    for x1, y1, x2, y2, conf, cls in zip(boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3], scores, classes):
                        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                        label = self.model.names[int(cls)]

                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)

                        cv2.circle(cv_img, (center_x, center_y), 5, (0, 255, 0), -1)
                        cv2.rectangle(cv_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(cv_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                        cv2.putText(cv_img, str(center_y / 1 - coordinates[0][1]) + '^', (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                        cv2.putText(cv_img, str(center_x / 1 - coordinates[0][0]) + '>', (x1 - 90, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                for i in coordinates:
                    cv2.circle(cv_img, (i[0], i[1]), 5, (0, 255, 0), -1)
                    print("Координаты:", i)

                self.change_pixmap_signal.emit(cv_img)

        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Сохранение координат")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.disply_width = 640
        self.display_height = 480
        self.image_label = QLabel()
        self.image_label.resize(self.disply_width, self.display_height)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.central_widget.setLayout(vbox)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            coordinates.append((x, y))
            print("Координаты сохранены:", coordinates[-1])

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio))

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)  # Use QImage instead of QtGui.QImage
        p = QPixmap.fromImage(convert_to_Qt_format)
        return p


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
