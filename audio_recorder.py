import pyaudio
import wave

class AudioRecorder:
    def __init__(self, output_file="output_audio.wav", record_seconds=120, device_index=None):
        self.output_file = output_file
        self.record_seconds = record_seconds
        self.device_index = device_index

    def record_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        audio = pyaudio.PyAudio()

        if self.device_index is None:
            self.device_index = self.find_device_index()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True, 
                            input_device_index=self.device_index,
                            frames_per_buffer=CHUNK)
        
        print("Începere înregistrare audio...")
        frames = []
        
        for _ in range(0, int(RATE / CHUNK * self.record_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("Înregistrare audio completă.")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.output_file, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
    def find_device_index(self):
        audio = pyaudio.PyAudio()
        for i in range(audio.get_device_count()):
            if "Stereo Mix" in audio.get_device_info_by_index(i).get("name", ""):
                print(f"Found 'Stereo Mix' at index {i}")
                return i
        print("Stereo Mix not found, using default input.")
        return None
