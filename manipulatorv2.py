import cv2
import numpy as np

# Инициализация камеры
cap = cv2.VideoCapture(0)

while True:
    # Захват изображения с камеры
    ret, frame = cap.read()
    
    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Поиск краев на изображении с помощью оператора Canny
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Поиск прямых линий с помощью преобразования Хафа
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    # Рисование найденных линий на исходном изображении
    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Отображение результатов
    cv2.imshow('Detected lines', frame)
    
    # Для выхода нажмите 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
