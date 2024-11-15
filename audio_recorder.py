import sounddevice as sd
import numpy as np
import soundfile as sf
import threading

class AudioRecorder:
    def __init__(self, output_file="output_audio.wav", duration=120, sample_rate=44100, chunk_duration=1):
        self.output_file = output_file
        self.duration = duration
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.stop_event = threading.Event()

    def start_recording(self):
        print("\u00cencepem \u00eenregistrarea audio...")
        audio_data = []

        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1) as mic:
                for _ in range(int(self.duration // self.chunk_duration)):
                    if self.stop_event.is_set():
                        break
                    chunk = mic.read(int(self.sample_rate * self.chunk_duration))[0]
                    audio_data.append(chunk.flatten())
        except Exception as e:
            print(f"Eroare la \u00eenregistrarea audio: {e}")

        if audio_data:
            full_audio = np.concatenate(audio_data, axis=0)
            sf.write(self.output_file, full_audio, self.sample_rate)
            print(f"\u00cenregistrare audio finalizat\u0103 \u0219i salvat\u0103: {self.output_file}")

    def stop_recording(self):
        self.stop_event.set()
        print("\u00cencepem oprirea \u00eenregistr\u0103rii audio.")
