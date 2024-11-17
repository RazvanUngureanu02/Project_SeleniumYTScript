import threading
from youtube_browser import YouTubeBrowser
from youtube_gui import YouTubeGUI
from recorder import Recorder
import logging

# Configurăm logging-ul
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("application.log"),  # Logurile sunt salvate în fișierul application.log
        logging.StreamHandler()  # Logurile sunt afișate și în consolă
    ]
)
logger = logging.getLogger("Main")  # Logger principal pentru acest script

def main():
    """
    Funcția principală care inițializează aplicația.
    Configurează browser-ul, lansează interfața grafică, 
    gestionează înregistrările și închiderea browser-ului.
    """
    # Configurăm driver-ul pentru browser
    driver_path = 'C:\\Users\\2021 august\\Desktop\\ChromeDriver\\chromedriver.exe'
    logger.info("Pornim aplicația și configurăm driver-ul pentru browser.")
    try:
        # Inițializăm instanța YouTubeBrowser cu calea către ChromeDriver
        yt_browser = YouTubeBrowser(driver_path)
    except Exception as e:
        # Înregistrăm erorile critice care pot apărea la inițializarea browser-ului
        logger.critical(f"Eroare la configurarea browser-ului: {e}")
        return

    try:
        # Lansăm interfața grafică
        logger.info("Lansăm interfața grafică.")
        gui = YouTubeGUI(yt_browser)  # Creăm o instanță a interfeței grafice
        video_url, duration = gui.create_gui()  # Obținem URL-ul videoclipului și durata de la utilizator

        # Înregistrăm datele introduse de utilizator
        logger.info(f"URL/Nume videoclip introdus: {video_url}")
        logger.info(f"Durata înregistrării: {duration} secunde")

        # Configurăm Recorder-ul
        logger.info("Configurăm Recorder-ul.")
        recorder = Recorder(duration=int(duration), browser=yt_browser)  # Instanțiem Recorder-ul

        # Deschidem sau căutăm videoclipul în funcție de input
        try:
            # Verificăm dacă URL-ul curent din browser nu este deja un videoclip YouTube
            if not yt_browser.driver.current_url.startswith("https://www.youtube.com/watch"):
                if video_url.startswith("http"):  # Dacă utilizatorul a introdus un URL valid
                    logger.info(f"Deschidem URL-ul videoclipului: {video_url}")
                    yt_browser.open_video_url(video_url)  # Deschidem URL-ul în browser
                else:
                    # Dacă utilizatorul a introdus un termen de căutare
                    logger.info(f"Căutăm și redăm videoclipul după termenul de căutare: {video_url}")
                    yt_browser.search_and_play(video_url)  # Căutăm și redăm primul rezultat
        except Exception as e:
            # Înregistrăm erorile apărute la deschiderea sau căutarea videoclipului
            logger.error(f"Eroare la deschiderea sau căutarea videoclipului: {e}")
            return

        # Creăm un thread pentru înregistrare
        logger.info("Creăm un thread pentru înregistrare.")
        record_thread = threading.Thread(target=recorder.start_recording)  # Inițializăm un thread pentru înregistrare

        # Pornim înregistrarea
        logger.info("Pornim înregistrarea audio și capturarea cadrelor.")
        record_thread.start()  # Pornim thread-ul
        record_thread.join()  # Așteptăm să se termine înregistrarea

        logger.info("Înregistrările au fost finalizate.")

    except Exception as e:
        # Înregistrăm orice eroare care apare în timpul execuției aplicației
        logger.error(f"A apărut o eroare în timpul execuției aplicației: {e}")

    finally:
        try:
            # Închidem browser-ul dacă este deschis
            logger.info("Închidem browser-ul, dacă este încă activ.")
            yt_browser.close()  # Închidem browser-ul YouTube
        except Exception as e:
            # Înregistrăm erorile apărute la închiderea browser-ului
            logger.error(f"Eroare la închiderea browser-ului: {e}")
        # Notificăm că aplicația s-a încheiat
        logger.info("Aplicația s-a încheiat.")

if __name__ == "__main__":
    # Pornim aplicația apelând funcția principală
    logger.info("Pornim funcția principală.")
    main()
