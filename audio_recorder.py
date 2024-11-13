import sounddevice as sd
import numpy as np
import soundfile as sf
import threading

class AudioRecorder:
    def __init__(self, output_file="output_audio.wav", record_seconds=120, sample_rate=44100, chunk_duration=1):
        self.output_file = output_file
        self.record_seconds = record_seconds
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.stop_event = threading.Event()

    def start_recording(self):
        print("\u00cencepem \u00eenregistrarea audio...")
        data = []

        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1) as mic:
                for _ in range(int(self.record_seconds // self.chunk_duration)):
                    if self.stop_event.is_set():
                        break
                    chunk = mic.read(int(self.sample_rate * self.chunk_duration))[0]
                    data.append(chunk.flatten())
        except Exception as e:
            print(f"Eroare la \u00eenregistrarea audio: {e}")

        if data:
            full_data = np.concatenate(data, axis=0)
            sf.write(self.output_file, full_data, self.sample_rate)
            print(f"\u00cenregistrare audio completat\u0103 \u0219i salvat\u0103 la: {self.output_file}")

    def stop_recording(self):
        print("Oprire \u00eenregistrare audio.")
        self.stop_event.set()
