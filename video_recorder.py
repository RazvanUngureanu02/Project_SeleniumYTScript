import mss
import numpy as np
import cv2
import time
from concurrent.futures import ThreadPoolExecutor

class VideoRecorder:
    def __init__(self, output_file="output_video.mp4", duration=120, fps=30):
        self.output_file = output_file
        self.duration = duration
        self.fps = fps
        self.recording = False

    def start_recording(self):
        print("Începem înregistrarea video...")
        sct = mss.mss()
        monitor = sct.monitors[1]  # Monitorul principal
        frames = []

        start_time = time.time()
        while time.time() - start_time < self.duration:
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            frames.append(frame)

        print("Înregistrarea video a fost completată. Salvăm cadrele în fișier...")

        # Salvare cadre și generare video
        with ThreadPoolExecutor(max_workers=4) as executor:
            for i, frame in enumerate(frames):
                executor.submit(cv2.imwrite, f"frame_{i:04d}.png", frame)

        # Creare video folosind ffmpeg
        try:
            import subprocess
            subprocess.run([
                "ffmpeg", "-framerate", str(self.fps), "-i", "frame_%04d.png",
                "-vcodec", "libx264", "-pix_fmt", "yuv420p", self.output_file
            ])
            print(f"Fișierul video a fost salvat: {self.output_file}")
        except Exception as e:
            print(f"Eroare la generarea fișierului video: {e}")

    def stop_recording(self):
        self.recording = False
