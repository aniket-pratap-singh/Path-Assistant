import cv2
import time
from ultralytics import YOLO
import pyttsx3
import random

# Load YOLOv8 model (lightweight version)
model = YOLO('yolov8n.pt')  # You can use 'yolov8s.pt' for better accuracy

# Text-to-speech engine
engine = pyttsx3.init()

# Funny messages
messages = [
    "Zoomies in progress!",
    "This couch is mine now.",
    "Plotting something evil...",
    "Sniff detected! Hide your socks!",
    "I'm not fat, I'm fluffy.",
    "Suspicious activities going on...",
    "You didn’t see me eat that.",
    "I demand treats. Now.",
    "Why are you watching me?",
    "That wasn't me. It was the cat.",
]

# Webcam input
cap = cv2.VideoCapture(0)
last_spoken_time = 0
speak_delay = 5  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    pet_detected = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label in ['dog', 'cat']:
                pet_detected = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                caption = random.choice(messages)

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 200), 2)
                cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                # Show funny caption
                cv2.putText(frame, caption, (10, 40),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

                # Speak the caption every few seconds
                if time.time() - last_spoken_time > speak_delay:
                    engine.say(caption)
                    engine.runAndWait()
                    last_spoken_time = time.time()

    if not pet_detected:
        cv2.putText(frame, "No pet detected 🐾", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 255), 2)

    # Show the video feed
    cv2.imshow("Pet Gesture Interpreter 🐶😺", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
