import cv2
import os
import yt_dlp

def get_video_stream(url):
    ydl_opts = {
        'quiet': True,
        'format': 'best[ext=mp4]'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info['url']
    
    return stream_url

def stream_youtube_video(url):
    cap = None
    try:
        stream_url = get_video_stream(url)
        cap = cv2.VideoCapture(stream_url)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:  
        cap.release()
        cv2.destroyAllWindows()

def main_camera():
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



def downloads():
    cap = None
    try:
        video_path = 'C:/Users/prata/OneDrive/Desktop/Path Assitant/src/myvideo.mp4'
        if not video_path or not os.path.exists(video_path):
            print("Video not found after download.")
            return
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Not Successfully grabbed frame")
                break
            yield frame
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

