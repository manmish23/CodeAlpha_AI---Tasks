print("1. Starting script...")
import cv2
print("2. OpenCV imported")
from ultralytics import YOLO
print("3. YOLO imported")

model = YOLO('yolov8n.pt')
print("4. Model loaded")

cap = cv2.VideoCapture(0)
print("5. Webcam opened:", cap.isOpened())

if not cap.isOpened():
    print("ERROR: Cannot open webcam. Close other apps like Zoom/Teams.")
    exit()

print("6. Starting loop. Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Can't read frame")
        break

    results = model.track(frame, persist=True, conf=0.5)
    annotated_frame = results[0].plot()
    cv2.imshow("Task 4 - Webcam Tracking", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("7. Script ended")