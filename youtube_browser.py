from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class YouTubeBrowser:
    def __init__(self, driver_path):
        service = webdriver.chrome.service.Service(driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
    
    def open_youtube(self):
        self.driver.get("https://www.youtube.com")
        print("Opening YouTube")
        time.sleep(3)
    
    def accept_consent(self):
        try:
            self.driver.execute_script("""
                let buttons = document.querySelectorAll('button');
                for (let button of buttons) {
                    if (button.innerText.includes('Reject all') || button.innerText.includes('Accept all')) {
                        button.click();
                        break;
                    }
                }
            """)
            print("Am apăsat pe butonul de consimțământ ('Reject all' sau 'Accept all') folosind JavaScript.")
            time.sleep(3)  # Așteaptă ca pagina să se actualizeze după consimțământ
        except Exception as e:
            print("Nu am reușit să apăs pe butonul de consimțământ:", e)
    
    def open_video_url(self, video_url):
        """Deschide un URL specific către videoclipul YouTube."""
        self.driver.get(video_url)
        print(f"Deschidem videoclipul la URL-ul: {video_url}")
        time.sleep(5)  # Așteaptă câteva secunde pentru a permite încărcarea completă a videoclipului
    
    def close(self):
        self.driver.quit()
        print("Am închis browserul.")
