import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Изначальные размеры окна
        self.width = 1280
        self.height = 720

        # Создание горизонтального макета для изображений и кнопок
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Выравниваем элементы по центру

        # Путь к вашей папке с изображениями
        self.image_folder_path = r"D:\prosto\manipulator\images"

        # Создаем таймер для проверки папки с изображениями
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_image_folder)
        self.timer.start(1000)  # Проверяем каждую секунду

        # Функция для автоматического поиска изображений в папке
        self.image_paths = self.find_images_in_folder(self.image_folder_path)

        # Если изображений нет, добавить надпись "Не найдено"
        if not self.image_paths:
            label = QLabel("Изображения не найдены")
            label.setAlignment(Qt.AlignCenter)  # Выравниваем надпись по центру
            self.layout.addWidget(label)
        else:
            # Создаем вертикальный макет для изображений и кнопок слева
            left_layout = QVBoxLayout()
            left_layout.setAlignment(Qt.AlignCenter)

            # Создаем вертикальный макет для изображений и кнопок справа
            right_layout = QVBoxLayout()
            right_layout.setAlignment(Qt.AlignCenter)

            # Создание QLabel для каждой из картинок и добавление их в соответствующий макет
            self.labels = []
            self.buttons = []
            for i, path in enumerate(self.image_paths):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    label = QLabel()
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)  # Выравниваем изображение по центру
                    button = QPushButton(f"Button {i+1}")
                    if i % 2 == 0:
                        left_layout.addWidget(label)
                        left_layout.addWidget(button)
                    else:
                        right_layout.addWidget(label)
                        right_layout.addWidget(button)
                    self.labels.append(label)
                    self.buttons.append(button)

            # Добавляем вертикальные макеты в горизонтальный макет
            self.layout.addLayout(left_layout)
            self.layout.addLayout(right_layout)

        self.setLayout(self.layout)
        self.setWindowTitle('GUI с картинками и кнопками')

        # Устанавливаем начальные размеры окна
        self.resize(self.width, self.height)
        self.show()

    def find_images_in_folder(self, folder_path):
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']  # Расширения изображений
        image_paths = []

        # Проходим по всем файлам в папке
        for file_name in os.listdir(folder_path):
            # Получаем полный путь к файлу
            file_path = os.path.join(folder_path, file_name)
            # Проверяем, является ли файл изображением по расширению
            if any(file_name.endswith(ext) for ext in image_extensions):
                image_paths.append(file_path)

        return image_paths

    def check_image_folder(self):
        # При обновлении проверяем папку с изображениями и обновляем список изображений
        new_image_paths = self.find_images_in_folder(self.image_folder_path)
        if new_image_paths != self.image_paths:
            self.update_layout(new_image_paths)

    def update_layout(self, new_image_paths):
        # Удаляем старые QLabel и QPushButton
        for label in self.labels:
            label.setParent(None)
        for button in self.buttons:
            button.setParent(None)

        # Если изображений нет, добавить надпись "Не найдено"
        if not new_image_paths:
            label = QLabel("Изображения не найдены")
            label.setAlignment(Qt.AlignCenter)  # Выравниваем надпись по центру
            self.layout.addWidget(label)
        else:
            # Создаем вертикальный макет для изображений и кнопок слева
            left_layout = QVBoxLayout()
            left_layout.setAlignment(Qt.AlignCenter)

            # Создаем вертикальный макет для изображений и кнопок справа
            right_layout = QVBoxLayout()
            right_layout.setAlignment(Qt.AlignCenter)

            # Создание QLabel для каждой из картинок и добавление их в соответствующий макет
            self.labels = []
            self.buttons = []
            for i, path in enumerate(new_image_paths):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    label = QLabel()
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)  # Выравниваем изображение по центру
                    button = QPushButton(f"Button {i+1}")
                    if i % 2 == 0:
                        left_layout.addWidget(label)
                        left_layout.addWidget(button)
                    else:
                        right_layout.addWidget(label)
                        right_layout.addWidget(button)
                    self.labels.append(label)
                    self.buttons.append(button)

            # Добавляем вертикальные макеты в горизонтальный макет
            self.layout.addLayout(left_layout)
            self.layout.addLayout(right_layout)

        self.setWindowTitle('GUI с картинками и кнопками')

        # Перерисовываем изображения при изменении размеров окна
        self.redraw_images()

    # Переопределяем метод изменения размеров окна
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Перерисовываем изображения при изменении размеров окна
        self.redraw_images()

    def redraw_images(self):
        if self.labels:
            for label in self.labels:
                pixmap = label.pixmap()
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio)
                    label.setPixmap(scaled_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())
 