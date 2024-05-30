import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QInputDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Разделение экрана")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаем GridLayout
        self.layout = QGridLayout(central_widget)

        # Добавляем виджеты в каждую из трех ячеек GridLayout
        self.widget1 = QWidget()
        self.widget1.setStyleSheet("background-color: red;")
        self.layout.addWidget(self.widget1, 0, 0, 1, 1)  # (row, column, rowspan, columnspan)

        self.widget2 = QWidget()
        self.widget2.setStyleSheet("background-color: green;")
        self.layout.addWidget(self.widget2, 0, 1, 1, 1)

        self.widget3 = QWidget()
        self.widget3.setStyleSheet("background-color: blue;")
        self.layout.addWidget(self.widget3, 0, 2, 1, 1)

        # Кнопка для вызова диалогового окна
        self.button = QPushButton("Изменить разделители", self)
        self.button.clicked.connect(self.changeDividers)
        self.layout.addWidget(self.button, 1, 0, 1, 3)  # Кнопка занимает всю ширину


    def updateGridLayout(self, num_columns):
        # Удаляем все виджеты из layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Добавляем виджеты в каждую из num_columns колонок
        for i in range(num_columns):
            widget = QWidget()
            widget.setStyleSheet("background-color: red;")
            self.layout.addWidget(widget, 0, i, 1, 1)

    def changeDividers(self):
        num_columns, ok = QInputDialog.getInt(self, "Изменение разделителей", "Введите количество разделителей:",
                                              min=1, max=10, value=self.layout.columnCount())
        if ok:
            self.updateGridLayout(num_columns)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)  # Задаем размеры окна
    window.show()
    sys.exit(app.exec_())
