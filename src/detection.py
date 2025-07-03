from camera import main_camera as main
from camera import downloads as downloads
from camera import stream_youtube_video as stream
import cv2
from ultralytics import YOLO

model1=YOLO("models/road_detector.pt")
model2=YOLO("models/yolov8n.pt")

def main_detection(frame):
    result1=model1(frame, verbose=False)
    result2=model2(frame, verbose=False)
    annotated_frame=frame.copy()
    detection1=[]
    detection2=[]

    for box in result1[0].boxes:
        class_id=int(box.cls[0])
        class_name=model1.names[class_id]
        confidence=float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(annotated_frame, f"{class_name} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        # print(f"Road Detection: {class_name} with confidence {confidence}")
        detection1.append((class_name, confidence))
        
    for box in result2[0].boxes:
        class_id=int(box.cls[0])
        class_name=model2.names[class_id]
        confidence=float(box.conf[0])
        detection2.append((class_name, confidence))
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"{class_name} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    resized_frame = cv2.resize(annotated_frame, (800, 600))
    cv2.imshow("Unified Detection", resized_frame)

    return detection1, detection2




def detect():
    for frame in downloads():
        detection1, detection2=main_detection(frame)
        yield detection1, detection2
        
        
# yt-dlp -f mp4 -o "C:/Users/prata/OneDrive/Desktop/Path Assitant/src/myvideo.mp4" "url"



