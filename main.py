import tkinter as tk
from youtube_browser import YouTubeBrowser
from video_recorder import VideoRecorder
from audio_recorder import AudioRecorder
import threading

def get_video_url():
    root = tk.Tk()
    root.title("Introduceți URL-ul videoclipului YouTube")
    root.geometry("400x150")
    
    label = tk.Label(root, text="Introduceți URL-ul videoclipului YouTube:")
    label.pack(pady=10)

    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    def submit():
        global video_url
        video_url = url_entry.get()
        root.destroy()
    
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack(pady=10)
    root.mainloop()

def main():
    get_video_url()
    
    driver_path = 'C:\\Users\\2021 august\\Desktop\\ChromeDriver\\chromedriver.exe'
    yt_browser = YouTubeBrowser(driver_path)
    video_recorder = VideoRecorder(duration=120)
    audio_recorder = AudioRecorder(record_seconds=120)

    yt_browser.open_youtube()
    yt_browser.accept_consent()
    yt_browser.open_video_url(video_url)

    # Începerea înregistrării audio și video în thread-uri
    video_thread = threading.Thread(target=video_recorder.start_recording)
    audio_thread = threading.Thread(target=audio_recorder.record_audio)

    video_thread.start()
    audio_thread.start()

    video_thread.join()
    audio_thread.join()

    yt_browser.close()

if __name__ == "__main__":
    main()
