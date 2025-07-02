from camera import main
import cv2
from ultralytics import YOLO
model1=YOLO("road_detector.pt")
model2=YOLO("yolov8n.pt")

def detect(frame):
    result1=model1(frame, verbose=False)
    result2=model2(frame, verbose=False)
    annotated_frame=result2[0].plot()
    return result1, result2

def main_detection():
    for frame in main():
        result1, result2=detect(frame)
        cv2.imshow("Detection", frame)
        detection1=[]
        detection2=[]
        for box in result1[0].boxes:
            class_id=int(box.cls[0])
            class_name=model1.names[class_id]
            confidence=float(box.conf[0])
            detection1.append((class_name, confidence))
        
        for box in result2[0].boxes:
            class_id=int(box.cls[0])
            class_name=model2.names[class_id]
            confidence=float(box.conf[0])
            detection2.append((class_name, confidence))
        yield detection1, detection2
        
            
        
        

