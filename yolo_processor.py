import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Сохранение координат")
        self.setGeometry(100, 100, 400, 300)

        self.coordinates = []

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x() * (1000 / self.size().width())
            y = event.y() * (1000 / self.size().height())
            self.coordinates.append((x, y))
            print("Координаты сохранены:", self.coordinates)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
