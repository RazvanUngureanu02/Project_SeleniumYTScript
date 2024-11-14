from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class YouTubeBrowser:
    def __init__(self, driver_path):
        service = webdriver.chrome.service.Service(driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

    def open_youtube(self):
        self.driver.get("https://www.youtube.com")
        print("Deschidem YouTube")
        time.sleep(3)

    def accept_consent(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                text = button.get_attribute("innerText").strip().lower()
                if "reject all" in text or "accept all" in text or "refuză tot" in text or "acceptă tot" in text:
                    button.click()
                    print(f"Am apăsat pe butonul de consimțământ: {text}")
                    time.sleep(2)
                    return
            print("Nu am găsit butoanele de consimțământ.")
        except Exception as e:
            print(f"Eroare la gestionarea consimțământului: {e}")

    def handle_ads(self):
        """Gestionează reclamele YouTube și apasă pe 'Skip Ad' doar dacă este disponibil."""
        try:
            while True:
                # Caută butonul "Skip Ad"
                skip_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ytp-ad-skip-button"))
                )
                if skip_button.is_displayed():
                    skip_button.click()
                    print("Am sărit peste reclamă.")
                    break
        except Exception as e:
            print("Nu există reclame de sărit sau s-a terminat redarea reclamei:", e)

    def open_video_url(self, video_url):
        """Deschide un URL specific către videoclipul YouTube."""
        self.driver.get(video_url)
        print(f"Deschidem videoclipul la URL-ul: {video_url}")
        time.sleep(5)
        self.accept_consent()
        self.play_video()

    def play_video(self):
        """Redă videoclipul sau gestionați reclamele, dacă este necesar."""
        try:
            # Verifică dacă videoclipul este în redare sau dacă există reclame
            self.handle_ads()
            play_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ytp-play-button"))
            )
            if "Play" in play_button.get_attribute("aria-label"):
                play_button.click()
                print("Am dat play automat la videoclip.")
            else:
                print("Videoclipul este deja în redare.")
        except Exception as e:
            print("Nu am reușit să redau videoclipul sau să gestionez reclamele:", e)

    def search_and_play(self, query):
        """Caută un videoclip pe YouTube și redă primul rezultat."""
        self.driver.get(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        print(f"Căutăm: {query}")
        time.sleep(5)
        self.accept_consent()  # Asigură trecerea de consimțământ
        try:
            # Selectează și redă primul rezultat
            first_result = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@id="video-title"]'))
            )
            first_result.click()
            print("Redăm primul rezultat al căutării.")
            time.sleep(5)
            self.handle_ads()  # Gestionează reclamele după selectarea videoclipului
        except Exception as e:
            print("Eroare la căutarea sau redarea videoclipului:", e)

    def close(self):
        self.driver.quit()
        print("Am închis browserul.")
