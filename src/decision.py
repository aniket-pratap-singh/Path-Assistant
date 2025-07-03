# from src.detection import detect
from speak import speak
from detection import detect
import cv2
import numpy as np

obstacles_total = {"Road", "person", "bicycle", "car", "motorcycle", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear",
    "zebra", "giraffe", "chair", "couch", "potted plant", "bed", "dining table",
    "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush"}

home_obstacles_total = {"person", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "sink", "refrigerator", "dog", "cat"}
    
road_obstacles_total ={"person", "bicycle", "car", "airplane", "motorcycle", "bus", "train", "truck", "traffic", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow"}



def main_decision(detection1, detection2):
    all_detections = detection1 + detection2

    detected_classes = [obj[0] for obj in all_detections]
    road_conf = next((obj[1] for obj in detection1 if obj[0] == 'Road'), 0)
    person_conf = next((obj[1] for obj in detection2 if obj[0] == 'person'), 0)

    road_obstacles = [obj for obj in all_detections if obj[0] in road_obstacles_total]
    home_obstacles = [obj for obj in all_detections if obj[0] in home_obstacles_total]
    obstacle_present = [obj for obj in all_detections if obj[0] in obstacles_total]


    if road_conf > 0.8 and len(obstacle_present) == 1:
        message="Clear path detected — looks like an open road or wall, be cautious."
    elif 0.45 < road_conf <= 0.8 and len(road_obstacles) == 0 and len(home_obstacles) == 0:
        message="Probably an empty road, but be cautious."
    elif len(home_obstacles) > len(road_obstacles) and road_conf > 0.5 :
        message="It seems like you're indoors with some obstacles — walk carefully."
    elif len(road_obstacles) > len(home_obstacles) and road_conf > 0.5 :
        message="Looks like an outdoor road with traffic — proceed carefully."
    elif 'road' in obstacle_present and len(road_obstacles) > len(home_obstacles) and road_conf <= 0.5 :
        message="Not able to find clear space, might be a busy road — Stay in place."
    elif 'road' in obstacle_present and len(home_obstacles) > len(road_obstacles) and road_conf <= 0.5 :
        message="Not able to find clear space, might be indoors with obstacles — Stay in place."
    elif person_conf>0.8 and ((len(road_obstacles) == 1 and len(home_obstacles) == 1) or road_conf <= 0.8):
        message="Person detected in front — be cautious and move a bit."
    # elif len(road_obstacles) > len(home_obstacles) and person_conf>0.8 and ((len(road_obstacles) == 0 and len(home_obstacles) == 0) or road_conf > 0.8):
    #     message="Person detected nearby — be cautious and proceed carefully."
    elif len(home_obstacles)==len(road_obstacles) and person_conf<0.5 and road_conf>0.5:
        message="Looks like an outdoor road with traffic — proceed carefully."

    else:
        message="Not able to detect properly or this is night. — Stay in place."
         
    print(message)
    speak(message)
    


def decision():
    try:
        for detection1, detection2 in detect():
            main_decision(detection1, detection2)
    except KeyboardInterrupt:
        print("⛔ Interrupted by user")
        cv2.destroyAllWindows()
            


decision()