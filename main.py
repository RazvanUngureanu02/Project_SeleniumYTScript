import threading
from youtube_browser import YouTubeBrowser
from youtube_gui import YouTubeGUI
from recorder import Recorder

def main():
    # Configurăm driver-ul pentru browser
    driver_path = 'C:\\Users\\2021 august\\Desktop\\ChromeDriver\\chromedriver.exe'
    yt_browser = YouTubeBrowser(driver_path)

    try:
        # Lansăm interfața grafică
        print("Pornim aplicația GUI...")
        gui = YouTubeGUI(yt_browser)
        video_url, duration = gui.create_gui()

        print(f"URL/Nume videoclip introdus: {video_url}")
        print(f"Durata înregistrării: {duration} secunde")

        # Configurăm Recorder-ul
        recorder = Recorder(duration=int(duration), browser=yt_browser)

        # Deschidem sau căutăm videoclipul în funcție de input
        if not yt_browser.driver.current_url.startswith("https://www.youtube.com/watch"):
            if video_url.startswith("http"):
                yt_browser.open_video_url(video_url)
            else:
                yt_browser.search_and_play(video_url)

        # Creăm un thread pentru înregistrare
        record_thread = threading.Thread(target=recorder.start_recording)

        # Pornim înregistrarea
        print("Pornim înregistrarea audio și capturarea cadrelor...")
        record_thread.start()
        record_thread.join()

        print("Înregistrările au fost finalizate.")

    except Exception as e:
        print(f"A apărut o eroare: {e}")

if __name__ == "__main__":
    main()
