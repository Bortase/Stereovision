from ultralytics import YOLO
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        # Load the YOLOv8 model
        self.model = YOLO(r'G:\stereovision\runs\detect\train2\weights\best.pt')
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.results = self.model(cv_img)
                
                    # Process the results
                for result in self.results:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    scores = result.boxes.conf.cpu().numpy()
                    classes = result.boxes.cls.cpu().numpy()

                    # Iterate over the detections
                    for x1, y1, x2, y2, conf, cls in zip(boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3], scores, classes):
                        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                        label = self.model.names[int(cls)]

                        # Display the bounding box and label
                        print('x:', label, (x1 + x2) / 2, 'y', (y1 + y2) / 2)

                        # Calculate the center of the bounding box
                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)

                        # Draw a circle at the center of the bounding box
                        cv2.circle(cv_img, (center_x, center_y), 5, (0, 255, 0), -1)

                        # Draw the bounding box and label
                        cv2.rectangle(cv_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(cv_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                        cv2.putText(cv_img, str(48 - center_y / 10) + '^', (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                        cv2.putText(cv_img, str(center_x / 10) + '>', (x1 - 90, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)

        # create a vertical box layout and add the label
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        # set the vbox layout as the widget's layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def resizeEvent(self, event):
        # When the window is resized, update the image_label size
        self.disply_width = self.image_label.width()
        self.display_height = self.image_label.height()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio))

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
