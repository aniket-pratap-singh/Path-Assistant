import cv2
def main():
    try:
        cap=cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame= cap.read()

            if not ret:
                print("Failed to grab frame")
                break
            frame = cv2.flip(frame, 1)
            yield(frame)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
