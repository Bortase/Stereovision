import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame, QSizePolicy, QSplitter, QSlider, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from ultralytics import YOLO

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    update_objects_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        model = YOLO('yolov8n.pt')
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                results = model(frame)
                annotated_frame = results[0].plot()
                detected_objects = []
                for box in results[0].boxes.data:
                    x1, y1, x2, y2, conf, cls = box
                    cls = int(cls)
                    label = model.names[cls]
                    object_image = frame[int(y1):int(y2), int(x1):int(x2)]
                    detected_objects.append((label, object_image))
                self.change_pixmap_signal.emit(annotated_frame)
                self.update_objects_signal.emit(detected_objects)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Object Detection with YOLOv8")
        self.setGeometry(100, 100, 1200, 800)

        self.image_label = QLabel(self)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(200, 150)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setMinimumSize(200, 150)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.image_label)
        self.splitter.addWidget(self.scroll_area)
        self.splitter.setSizes([600, 200])

        self.slider = QSlider(Qt.Vertical)
        self.slider.setRange(50, 400)  # Минимальный и максимальный размер (в процентах)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.update_object_sizes)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.splitter)
        self.hbox.addWidget(self.slider)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.update_objects_signal.connect(self.update_objects)
        self.thread.start()

        self.current_objects = []

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img, self.image_label.width(), self.image_label.height())
        self.image_label.setPixmap(qt_img)

    def update_objects(self, objects):
        self.current_objects = objects  # Сохраняем текущие объекты для обновления их размеров
        self.refresh_objects()

    def refresh_objects(self):
        size_factor = self.slider.value() / 100.0  # Преобразуем значение ползунка в коэффициент размера
        button_height = int(30 * size_factor)  # Высота кнопки масштабируется вместе с изображениями
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for label, obj_img in self.current_objects:
            vbox = QVBoxLayout()
            img_label = QLabel()
            qt_img = self.convert_cv_qt(obj_img, int(200 * size_factor), int(200 * size_factor))
            img_label.setPixmap(qt_img)
            img_label.setAlignment(Qt.AlignCenter)
            button = QPushButton(label)
            button.setFixedHeight(button_height)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            vbox.addWidget(img_label)
            vbox.addWidget(button)
            vbox.setAlignment(button, Qt.AlignCenter)
            frame = QFrame()
            frame.setLayout(vbox)
            self.scroll_layout.addWidget(frame)

    def update_object_sizes(self):
        self.refresh_objects()  # Обновляем размеры объектов при изменении значения ползунка

    def convert_cv_qt(self, cv_img, width, height):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(width, height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
