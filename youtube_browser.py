import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurarea logger-ului pentru a înregistra mesajele în fișier și consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("application.log"),  # Log-urile vor fi salvate în application.log
        logging.StreamHandler()  # Log-urile vor fi afișate și în consolă
    ]
)
logger = logging.getLogger("YouTubeBrowserLogger")  # Creăm un logger pentru acest script

class YouTubeBrowser:
    def __init__(self, driver_path):
        """
        Inițializează browser-ul Chrome și maximizează fereastra.
        :param driver_path: Calea către executabilul ChromeDriver.
        """
        try:
            # Inițializăm serviciul ChromeDriver
            service = webdriver.chrome.service.Service(driver_path)
            # Creăm o instanță a browser-ului Chrome
            self.driver = webdriver.Chrome(service=service)
            # Maximizăm fereastra browser-ului
            self.driver.maximize_window()
            logger.info("Browser-ul Chrome a fost inițializat și maximizat.")
        except Exception as e:
            # Înregistrăm erorile critice dacă inițializarea eșuează
            logger.critical(f"Eroare la inițializarea browser-ului: {e}", exc_info=True)

    def open_youtube(self):
        """
        Deschide pagina principală a YouTube în browser.
        """
        try:
            # Navigăm către pagina principală a YouTube
            self.driver.get("https://www.youtube.com")
            logger.info("Pagina YouTube a fost deschisă cu succes.")
            # Așteptăm 3 secunde pentru a permite încărcarea completă
            time.sleep(3)
        except Exception as e:
            # Înregistrăm erorile dacă deschiderea paginii eșuează
            logger.error(f"Eroare la deschiderea YouTube: {e}", exc_info=True)

    def accept_consent(self):
        """
        Gestionează dialogurile de consimțământ, cum ar fi "Accept All" sau "Reject All".
        """
        try:
            # Așteptăm până ce apar butoanele în DOM
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
            # Căutăm toate elementele de tip "button" din pagină
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                # Obținem textul fiecărui buton și îl convertim în litere mici
                text = button.get_attribute("innerText").strip().lower()
                if "reject all" in text or "accept all" in text or "refuză tot" in text or "acceptă tot" in text:
                    # Apăsăm pe butonul corespunzător dacă găsim unul potrivit
                    button.click()
                    logger.info(f"Butonul de consimțământ apăsat: {text}")
                    time.sleep(2)  # Așteptăm 2 secunde pentru a finaliza acțiunea
                    return
            logger.warning("Nu s-au găsit butoanele de consimțământ.")
        except Exception as e:
            # Înregistrăm erorile dacă gestionarea consimțământului eșuează
            logger.error(f"Eroare la gestionarea consimțământului: {e}", exc_info=True)

    def handle_ads(self):
        """
        Gestionează reclamele YouTube prin apăsarea butonului "Skip Ad" dacă este prezent.
        """
        try:
            while True:
                # Căutăm butonul "Skip Ad" timp de 2 secunde
                skip_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ytp-ad-skip-button"))
                )
                if skip_button.is_displayed():
                    # Apăsăm pe butonul "Skip Ad" dacă este vizibil
                    skip_button.click()
                    logger.info("Reclama a fost sărită cu succes.")
                    break
        except Exception:
            # Nu înregistrăm o eroare, ci doar o informație dacă nu sunt reclame
            logger.info("Nu există reclame de sărit sau s-a terminat redarea reclamei.")

    def open_video_url(self, video_url):
        """
        Deschide un videoclip specific pe YouTube folosind URL-ul furnizat.
        :param video_url: URL-ul videoclipului YouTube de deschis.
        """
        try:
            if not video_url.startswith("http"):
                logger.warning("URL invalid pentru videoclipul YouTube.")
                return
            # Navigăm către URL-ul videoclipului
            self.driver.get(video_url)
            logger.info(f"Videoclipul a fost deschis cu URL-ul: {video_url}")
            time.sleep(5)  # Așteptăm 5 secunde pentru a permite încărcarea completă
            self.accept_consent()  # Gestionăm consimțământul dacă este necesar
            self.play_video()  # Redăm videoclipul
        except Exception as e:
            # Înregistrăm erorile dacă deschiderea videoclipului eșuează
            logger.error(f"Eroare la deschiderea URL-ului videoclipului: {e}", exc_info=True)

    def play_video(self):
        """
        Redă videoclipul dacă nu este deja în redare sau gestionează reclamele înainte de redare.
        """
        try:
            # Gestionăm reclamele înainte de a reda videoclipul
            self.handle_ads()
            # Căutăm butonul de redare în DOM
            play_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ytp-play-button"))
            )
            if "Play" in play_button.get_attribute("aria-label"):
                # Apăsăm pe butonul "Play" dacă videoclipul nu este deja în redare
                play_button.click()
                logger.info("Videoclipul a fost redat automat.")
            else:
                logger.info("Videoclipul este deja în redare.")
        except Exception as e:
            # Înregistrăm erorile dacă redarea videoclipului eșuează
            logger.error(f"Eroare la redarea videoclipului sau gestionarea reclamelor: {e}", exc_info=True)

    def search_and_play(self, query):
        """
        Caută un videoclip pe YouTube folosind o interogare text și redă primul rezultat.
        :param query: Interogarea text pentru căutarea videoclipului.
        """
        try:
            # Construim URL-ul pentru căutarea pe YouTube
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            self.driver.get(search_url)
            logger.info(f"Căutăm pe YouTube: {query}")
            time.sleep(5)  # Așteptăm 5 secunde pentru a permite încărcarea completă
            self.accept_consent()  # Gestionăm consimțământul dacă este necesar
            # Căutăm primul rezultat al căutării
            first_result = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@id="video-title"]'))
            )
            # Apăsăm pe primul rezultat
            first_result.click()
            logger.info("Primul rezultat al căutării a fost redat.")
            time.sleep(5)  # Așteptăm 5 secunde pentru a permite încărcarea completă
            self.handle_ads()  # Gestionăm reclamele dacă este necesar
        except Exception as e:
            # Înregistrăm erorile dacă căutarea sau redarea videoclipului eșuează
            logger.error(f"Eroare la căutarea sau redarea videoclipului: {e}", exc_info=True)

    def close(self):
        try:
            if self.driver.service.process:  # Verificăm dacă driver-ul este activ
                self.driver.quit()
                logger.info("Browser-ul Chrome a fost închis cu succes.")
            else:
                logger.warning("Browser-ul era deja închis.")
        except Exception as e:
            logger.error(f"Eroare la închiderea browser-ului: {e}", exc_info=True)