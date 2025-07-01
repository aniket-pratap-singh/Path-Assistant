from camera import main
import cv2
from ultralytics import YOLO
model=YOLO("yolov8n.pt")

def detect(frame):
    results=model(frame, verbose=False)
    annotated_frame=results[0].plot()
    return annotated_frame


for frame in main():
    frame_with_boxes=detect(frame)
    cv2.imshow("Detection", frame_with_boxes)

