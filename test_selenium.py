
from selenium import webdriver  # Permite controlul browserului
from selenium.common.exceptions import TimeoutException  # Gestionare excepții pentru timpi de așteptare
from selenium.webdriver.chrome.service import Service  # Setare cale către ChromeDriver
from selenium.webdriver.common.by import By  # Metode de localizare a elementelor pe pagină
from selenium.webdriver.common.keys import Keys  # Simulează apăsarea tastelor
from selenium.webdriver.support.ui import WebDriverWait  # Așteaptă elementele până devin accesibile
from selenium.webdriver.support import expected_conditions as EC  # Condiții pentru accesibilitatea elementelor
import time  # Adaugă pauze fixe în execuția codului

# Specifică calea corectă către executabilul ChromeDriver
service = Service('C:\\Users\\2021 august\\Desktop\\ChromeDriver\\chromedriver.exe')

# Inițializează driverul Chrome utilizând serviciul configurat
driver = webdriver.Chrome(service=service)

# Deschide YouTube
driver.get("https://www.youtube.com")
print("Opening " + driver.title)  # Afișează titlul paginii pentru confirmarea încărcării

# Așteaptă 3 secunde pentru a permite încărcarea completă a paginii și a pop-up-ului de consimțământ
time.sleep(3)

# Execută JavaScript pentru a găsi și face click pe butonul „Reject all” sau „Accept all”
try:
    driver.execute_script("""
        let buttons = document.querySelectorAll('button');  // Selectează toate butoanele de pe pagină
        for (let button of buttons) {  // Parcurge fiecare buton găsit
            if (button.innerText.includes('Reject all') || button.innerText.includes('Accept all')) {  
                // Verifică dacă textul butonului conține „Reject all” sau „Accept all”
                button.click();  // Face click pe butonul găsit
                break;  // Oprește căutarea după primul buton găsit
            }
        }
    """)
    print("Am apăsat pe butonul de consimțământ ('Reject all' sau 'Accept all') folosind JavaScript.")
except Exception as e:
    # În caz de eroare la găsirea butonului, afișează un mesaj de eroare
    print("Nu am reușit să apăs pe butonul de consimțământ folosind JavaScript:", e)

# Așteaptă alte 3 secunde pentru stabilizarea paginii după închiderea pop-up-ului
time.sleep(3)

# Caută bara de căutare și introduce titlul videoclipului
try:
    searchedItem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "search_query"))  # Așteaptă până când bara de căutare devine interactivă
    )
    searchedItem.send_keys("Ed Sheeran - Shape of You")  # Introduce titlul videoclipului în bara de căutare
    searchedItem.send_keys(Keys.RETURN)  # Apasă tasta Enter pentru a începe căutarea
    print("Am căutat videoclipul dorit.")
except TimeoutException:
    # În caz că bara de căutare nu este găsită, afișează un mesaj de eroare și închide browserul
    print("Bara de căutare nu a fost găsită.")
    driver.quit()
    exit()

# Așteaptă încărcarea rezultatelor și selectează videoclipul dorit
try:
    videoLink = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Ed Sheeran - Shape of You"))
        # Găsește un link parțial care conține textul „Ed Sheeran - Shape of You”
    )
    videoLink.click()  # Face click pe videoclipul găsit pentru a începe redarea
    print("Am dat click pe videoclipul dorit.")
except TimeoutException:
    # Dacă videoclipul nu este găsit în rezultate, afișează un mesaj de eroare și închide browserul
    print("Videoclipul nu a fost găsit în rezultate.")
    driver.quit()
    exit()

# Așteaptă 5 secunde pentru a vizualiza videoclipul și pentru a permite omitere automată a reclamelor (dacă există)
time.sleep(5)  # Pauză ajustabilă pentru durata reclamelor

# Închide browserul după finalizarea procesului
driver.quit()
print("Am închis browserul.")