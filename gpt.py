import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO(r'D:\stereovision1\stereovision\runs\detect\train2\weights\best.pt')



# Open the video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run the YOLO model on the frame
    results = model(frame)

    # Process the results
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()

        # Iterate over the detections
        for x1, y1, x2, y2, conf, cls in zip(boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3], scores, classes):
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            label = model.names[int(cls)]

            # Display the bounding box and label
            print('x:', label, (x1 + x2) / 2, 'y', (y1 + y2) / 2)

            # Calculate the center of the bounding box
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Draw a circle at the center of the bounding box
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            # Draw the bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.putText(frame, str(48 - center_y / 10) + '^', (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.putText(frame, str(center_x / 10) + '>', (x1 - 90, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close all windows
cap.release()
cv2.destroyAllWindows()