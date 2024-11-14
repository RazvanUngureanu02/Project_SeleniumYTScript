import os
import time
import threading
import cv2
import numpy as np
import mss
import soundcard as sc
import soundfile as sf
import subprocess


class Recorder:
    def __init__(self, duration, output_folder="Recordings"):
        self.duration = duration
        self.output_folder = output_folder
        self.audio_file = os.path.join(self.output_folder, "output_audio.mp3")
        self.frames_dir = os.path.join(self.output_folder, "frames")
        self.video_file = os.path.join(self.output_folder, "output_video.mp4")
        self.stop_event = threading.Event()

        # Creăm directoarele necesare
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)

    def record_audio(self):
        """Înregistrăm audio și salvăm în fișier MP3."""
        print("\nÎncepem înregistrarea audio...")
        data = []
        try:
            with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=44100) as mic:
                for _ in range(self.duration):
                    if self.stop_event.is_set():
                        break
                    chunk = mic.record(numframes=44100)
                    data.append(chunk[:, 0])
            if data:
                full_data = np.concatenate(data, axis=0)
                sf.write(self.audio_file, full_data, 44100, format="MP3")  # Salvăm ca MP3
                print(f"Audio-ul a fost salvat la: {self.audio_file}")
        except Exception as e:
            print(f"Eroare la înregistrarea audio: {e}")

    def capture_frames(self):
        """Capturăm cadrele din ecran la cea mai mare viteză posibilă."""
        print("\nÎncepem capturarea cadrelor...")
        screen_size = mss.mss().monitors[1]
        frame_count = 0
        start_time = time.time()

        with mss.mss() as sct:
            while time.time() - start_time < self.duration:
                if self.stop_event.is_set():
                    break
                # Capturăm un cadru
                img = sct.grab(screen_size)
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

                # Salvăm imediat fiecare cadru pe disc
                frame_path = os.path.join(self.frames_dir, f"frame_{frame_count:06d}.png")
                cv2.imwrite(frame_path, frame)
                frame_count += 1

        self.frames_count = frame_count  # Salvăm numărul total de cadre
        self.fps = frame_count / self.duration  # Calculăm framerate-ul
        print(f"Cadre capturate: {frame_count}, Framerate calculat: {self.fps:.2f} FPS")

    def assemble_video(self):
        """Asamblăm cadrele și audio-ul într-un fișier video MP4."""
        print("\nÎncepem asamblarea video...")
        try:
            ffmpeg_cmd = [
                "ffmpeg",
                "-framerate", str(self.fps),  # Utilizăm framerate-ul calculat
                "-i", os.path.join(self.frames_dir, "frame_%06d.png"),
                "-i", self.audio_file,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-pix_fmt", "yuv420p",
                "-shortest",
                self.video_file
            ]

            subprocess.run(ffmpeg_cmd, check=True)
            print(f"Fișierul video a fost salvat la: {self.video_file}")
        except subprocess.CalledProcessError as e:
            print(f"Eroare la asamblarea video: {e}")
        except Exception as e:
            print(f"Eroare generală: {e}")

        # Opțional: ștergem cadrele după asamblare
        for frame in os.listdir(self.frames_dir):
            os.remove(os.path.join(self.frames_dir, frame))
        os.rmdir(self.frames_dir)

    def start_recording(self):
        """Pornim înregistrarea audio și video."""
        audio_thread = threading.Thread(target=self.record_audio)
        video_thread = threading.Thread(target=self.capture_frames)

        print(f"\nPornim înregistrarea pentru {self.duration} secunde...")
        audio_thread.start()
        video_thread.start()

        audio_thread.join()
        video_thread.join()

        print("\nÎnregistrările au fost finalizate. Începem asamblarea...")
        self.assemble_video()


# Main pentru testare
if __name__ == "__main__":
    try:
        durata = int(input("Introduceți durata în secunde pentru înregistrare: "))
        recorder = Recorder(durata)
        recorder.start_recording()
    except ValueError:
        print("Introduceți un număr valid pentru durată.")
