import threading
from youtube_browser import YouTubeBrowser
from youtube_gui import create_gui
from audio_recorder import AudioRecorder
from video_recorder import VideoRecorder

def main():
    # Configurăm driver-ul pentru browser
    driver_path = 'C:\\Users\\2021 august\\Desktop\\ChromeDriver\\chromedriver.exe'
    yt_browser = YouTubeBrowser(driver_path)

    # Pornește interfața grafică și obține informațiile de la utilizator
    print("Pornim aplicația GUI...")
    video_url, duration = create_gui(yt_browser)

    print(f"URL/Nume videoclip introdus: {video_url}")
    print(f"Durata înregistrării: {duration} secunde")

    # Configurăm înregistratoarele audio și video
    audio_recorder = AudioRecorder(output_file="output_audio.wav", record_seconds=duration)
    video_recorder = VideoRecorder(output_file="output_video.avi", duration=duration)

    # Dacă a fost introdus un URL sau nume de căutare, deschidem/ căutăm videoclipul
    if not yt_browser.driver.current_url.startswith("https://www.youtube.com/watch"):
        if video_url.startswith("http"):
            yt_browser.open_video_url(video_url)
        else:
            yt_browser.search_and_play(video_url)

    # Creăm thread-uri pentru înregistrare audio și video
    audio_thread = threading.Thread(target=audio_recorder.start_recording)
    video_thread = threading.Thread(target=video_recorder.start_recording)

    # Pornim înregistrările
    print("Pornim înregistrarea audio și video...")
    audio_thread.start()
    video_thread.start()

    # Așteptăm ca ambele thread-uri să finalizeze
    audio_thread.join()
    video_thread.join()

    print("Înregistrările au fost finalizate.")
    yt_browser.close()

if __name__ == "__main__":
    main()
