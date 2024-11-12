import cv2
import numpy as np
import pyautogui
import time

class VideoRecorder:
    def __init__(self, output_file="output_video.avi", duration=120):
        self.output_file = output_file
        self.duration = duration
        self.recording = False
    
    def start_recording(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.output_file, fourcc, 10, screen_size)
        
        self.recording = True
        start_time = time.time()
        
        print("Începerea înregistrării video...")
        while self.recording and (time.time() - start_time < self.duration):
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        
        out.release()
        print("Înregistrarea video a fost oprită.")

    def stop_recording(self):
        self.recording = False
