from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Configurare cale pentru ChromeDriver
from selenium.webdriver.common.by import By  # Metode de localizare a elementelor
from selenium.webdriver.common.keys import Keys  # Control asupra tastelor precum Enter, Escape
from selenium.webdriver.support.ui import WebDriverWait  # Gestionare timpi de așteptare
from selenium.webdriver.support import expected_conditions as EC  # Condiții pentru elemente vizibile
from selenium.common.exceptions import TimeoutException  # Excepții pentru timpi de așteptare
import time  # Pauze între acțiuni

# Configurare cale pentru executabilul ChromeDriver
chrome_service = Service('C:\\Users\\2021 august\\Desktop\\ChromeDriver\\chromedriver.exe')

# Inițializare driver Chrome cu serviciul configurat
driver = webdriver.Chrome(service=chrome_service)

# Navighează pe YouTube
driver.get("https://www.youtube.com")
print("S-a deschis pagina:", driver.title)  # Afișează titlul paginii pentru confirmare

# Pauză de 3 secunde pentru a permite încărcarea completă a elementelor
time.sleep(3)

# Gestionare pop-up consimțământ (ex. Accept all)
try:
    # Așteaptă până când butonul „Accept all” devine vizibil și poate fi accesat
    accept_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//button[text()="Accept all"]'))
    )
    accept_button.click()  # Click pe butonul „Accept all” pentru a închide pop-up-ul
    print("Butonul de consimțământ a fost apăsat.")
except TimeoutException:
    print("Butonul de consimțământ nu a fost găsit. Continuăm fără această acțiune.")

# Caută bara de căutare pentru a introduce numele videoclipului
try:
    # Așteaptă până când bara de căutare devine interactivă
    search_bar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "search_query"))
    )
    search_bar.send_keys("Ed Sheeran - Shape of You")  # Trimite titlul videoclipului pentru căutare
    search_bar.send_keys(Keys.RETURN)  # Apasă Enter pentru a iniția căutarea
    print("Căutarea videoclipului a fost inițiată.")
except TimeoutException:
    print("Bara de căutare nu a fost găsită.")
    driver.quit()

# Pauză de 2 secunde pentru a permite încărcarea rezultatelor căutării
time.sleep(2)

# Caută și face click pe videoclipul dorit
try:
    # Găsește primul link care conține titlul parțial al videoclipului
    video_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Ed Sheeran - Shape of You"))
    )
    video_link.click()  # Click pe videoclip pentru a începe redarea
    print("Videoclipul a fost selectat și redarea a început.")
except TimeoutException:
    print("Videoclipul nu a fost găsit în rezultatele căutării.")
    driver.quit()

# Pauză pentru vizualizarea videoclipului sau omitere reclame, dacă există
time.sleep(5)

# Închidere browser la final
driver.quit()
print("Browserul a fost închis.")
