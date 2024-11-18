import os
import time
import threading
import cv2
import numpy as np
import mss
import soundcard as sc
import soundfile as sf
import subprocess
import logging

# Configurăm logging-ul
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("application.log"),  # Log-urile sunt salvate în fișierul application.log
        logging.StreamHandler()  # Log-urile sunt afișate și în consolă
    ]
)
logger = logging.getLogger("Recorder")  # Logger pentru acest modul

class Recorder:
    def __init__(self, duration, browser, output_folder="Recordings"):
        """
        Inițializează obiectul Recorder cu durata înregistrării, browser-ul asociat și folderul de output.
        Creează directoarele necesare pentru cadre și fișiere audio/video.
        """
        self.duration = duration  # Durata înregistrării, în secunde
        self.browser = browser  # Browser-ul asociat, utilizat pentru control
        self.output_folder = output_folder  # Folderul pentru salvarea fișierelor
        self.audio_file = os.path.join(self.output_folder, "output_audio.mp3")  # Calea fișierului audio
        self.frames_dir = os.path.join(self.output_folder, "frames")  # Folder pentru cadrele capturate
        self.video_file = os.path.join(self.output_folder, "output_video.mp4")  # Calea fișierului video final
        self.analysis_file = os.path.join(self.output_folder, "audio_analysis.txt")  # Calea raportului de analiză audio
        self.stop_event = threading.Event()  # Eveniment pentru oprirea proceselor

        # Creăm directoarele necesare dacă nu există
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            logger.info(f"Creat directorul pentru output: {self.output_folder}")
        if not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)
            logger.info(f"Creat directorul pentru cadre: {self.frames_dir}")

    def record_audio(self):
        """
        Înregistrează audio utilizând microfonul și salvează în format MP3.
        """
        logger.info("Pornim înregistrarea audio.")
        data = []
        try:
            # Începem capturarea audio de la microfon
            with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=44100) as mic:
                for _ in range(self.duration):
                    if self.stop_event.is_set():
                        logger.warning("Înregistrarea audio a fost oprită manual.")
                        break
                    chunk = mic.record(numframes=44100)  # Capturăm un buffer de date audio
                    data.append(chunk[:, 0])  # Adăugăm canalul mono în listă
            if data:
                full_data = np.concatenate(data, axis=0)  # Concatenăm toate datele înregistrate
                sf.write(self.audio_file, full_data, 44100, format="MP3")  # Salvăm fișierul audio
                logger.info(f"Audio-ul a fost salvat la: {self.audio_file}")
        except Exception as e:
            logger.error(f"Eroare la înregistrarea audio: {e}")

    def capture_frames(self):
        """
        Capturează cadrele ecranului la un framerate cât mai mare și le salvează ca imagini.
        """
        logger.info("Pornim capturarea cadrelor.")
        screen_size = mss.mss().monitors[1]  # Obținem dimensiunea monitorului principal
        frame_count = 0  # Numărăm cadrele capturate
        start_time = time.time()

        with mss.mss() as sct:
            while time.time() - start_time < self.duration:
                if self.stop_event.is_set():
                    logger.warning("Capturarea cadrelor a fost oprită manual.")
                    break
                try:
                    img = sct.grab(screen_size)  # Capturăm un cadru al ecranului
                    frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)  # Convertim imaginea în format RGB
                    frame_path = os.path.join(self.frames_dir, f"frame_{frame_count:06d}.png")  # Setăm calea fișierului
                    cv2.imwrite(frame_path, frame)  # Salvăm imaginea
                    frame_count += 1
                except Exception as e:
                    logger.error(f"Eroare la capturarea cadrului: {e}")

        self.frames_count = frame_count  # Salvăm numărul total de cadre capturate
        self.fps = frame_count / self.duration  # Calculăm framerate-ul
        logger.info(f"Cadre capturate: {frame_count}, Framerate calculat: {self.fps:.2f} FPS")

    def assemble_video(self):
        """
        Combină cadrele capturate și fișierul audio într-un videoclip MP4.
        """
        logger.info("Pornim procesul de asamblare video.")
        try:
            # Comanda FFmpeg pentru crearea videoclipului
            ffmpeg_cmd = [
                "ffmpeg",
                "-framerate", str(self.fps),
                "-i", os.path.join(self.frames_dir, "frame_%06d.png"),
                "-i", self.audio_file,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-pix_fmt", "yuv420p",
                "-shortest",
                self.video_file
            ]
            subprocess.run(ffmpeg_cmd, check=True)  # Executăm comanda FFmpeg
            logger.info(f"Fișierul video a fost salvat la: {self.video_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Eroare la asamblarea video: {e}")
        except Exception as e:
            logger.error(f"Eroare generală: {e}")
        finally:
            # Ștergem cadrele după asamblare
            for frame in os.listdir(self.frames_dir):
                os.remove(os.path.join(self.frames_dir, frame))
            os.rmdir(self.frames_dir)  # Ștergem directorul cadrelor
            logger.info("Directorul de cadre a fost curățat.")

    def analyze_audio(self):
        """
        Analizează nivelul sunetului din fișierul audio și generează un raport.
        """
        logger.info("Pornim analiza nivelului audio.")
        try:
            data, samplerate = sf.read(self.audio_file)  # Citim fișierul audio
            rms = np.sqrt(np.mean(np.square(data)))  # Calculăm nivelul RMS
            db_level = 20 * np.log10(rms) if rms > 0 else -np.inf  # Calculăm nivelul în decibeli
            # Scriem rezultatele analizei într-un fișier
            with open(self.analysis_file, "w") as f:
                f.write(f"Nivel RMS: {rms:.6f}\n")
                f.write(f"Nivel dB: {db_level:.2f} dB\n")
            logger.info(f"Analiza sunetului a fost salvată în: {self.analysis_file}")
        except Exception as e:
            logger.error(f"Eroare la analiza audio: {e}")

    def close_browser_after_duration(self):
        """
        Închide browser-ul asociat după finalizarea duratei înregistrării.
        """
        logger.info(f"Așteptăm {self.duration} secunde înainte de a închide browser-ul.")
        time.sleep(self.duration)
        try:
            self.browser.close()  # Închidem browser-ul
            self.browser.quit()  # Închidem complet procesul browser-ului
            logger.info("Browser-ul a fost închis automat.")
        except Exception as e:
            logger.error(f"Eroare la închiderea browser-ului: {e}")

    def start_recording(self):
        """
        Începe procesul de înregistrare audio, capturare video și închidere automată a browser-ului.
        """
        logger.info(f"Pornim procesul de înregistrare pentru {self.duration} secunde.")
        # Inițializăm thread-urile pentru audio, video și închiderea browser-ului
        audio_thread = threading.Thread(target=self.record_audio)
        video_thread = threading.Thread(target=self.capture_frames)
        close_browser_thread = threading.Thread(target=self.close_browser_after_duration)

        # Pornim thread-urile
        audio_thread.start()
        video_thread.start()
        close_browser_thread.start()

        # Așteptăm ca toate thread-urile să finalizeze execuția
        audio_thread.join()
        video_thread.join()
        close_browser_thread.join()

        logger.info("Înregistrările au fost finalizate. Începem procesul de asamblare.")
        self.assemble_video()  # Asamblăm videoclipul
        self.analyze_audio()  # Analizăm fișierul audio