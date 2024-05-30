import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import cv2
from ultralytics import YOLO

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the YOLOv8 model
        self.model = YOLO(r'G:\stereovision\runs\detect\train2\weights\best.pt')

        self.setWindowTitle("Video Stream")
        self.setGeometry(100, 100, 800, 600)

        # Create a label to display the video stream
        self.label = QLabel(self)
        self.label.move(10, 10)
        self.label.resize(640, 480)

        # Open the video capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        # Setup a timer to trigger the video stream
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 30)  # 30 FPS

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Run the YOLO model on the frame
        results = self.model(frame)

        # Process the results
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            scores = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()

            # Iterate over the detections
            for x1, y1, x2, y2, conf, cls in zip(boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3], scores, classes):
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                label = self.model.names[int(cls)]

                # Calculate the center of the bounding box
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # Draw a circle at the center of the bounding box
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

                # Draw the bounding box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Convert the frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to QImage
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

        # Convert the QImage to QPixmap
        pixmap = QPixmap.fromImage(image)

        # Update the label with the QPixmap
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        # Release resources and close the video capture
        self.cap.release()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoWindow()
    window.show()
    sys.exit(app.exec_())
