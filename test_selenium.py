from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import wave
import pyaudio
import cv2
import numpy as np

# Specifică calea corectă către ChromeDriver
service = Service('C:\\Users\\2021 august\\Desktop\\ChromeDriver\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Maximizează fereastra browserului
driver.maximize_window()

# Deschide YouTube
driver.get("https://www.youtube.com")
print("Opening " + driver.title)

time.sleep(3)  # Așteaptă pentru încărcare

# Găsește și face click pe „Reject all” sau „Accept all”
try:
    driver.execute_script("""
        let buttons = document.querySelectorAll('button');
        for (let button of buttons) {
            if (button.innerText.includes('Reject all') || button.innerText.includes('Accept all')) {
                button.click();
                break;
            }
        }
    """)
    print("Am apăsat pe butonul de consimțământ ('Reject all' sau 'Accept all') folosind JavaScript.")
except Exception as e:
    print("Nu am reușit să apăs pe butonul de consimțământ:", e)

time.sleep(3)

# Caută videoclipul
try:
    searchedItem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "search_query"))
    )
    searchedItem.send_keys("Ed Sheeran - Shape of You")
    searchedItem.send_keys(Keys.RETURN)
    print("Am căutat videoclipul dorit.")
except TimeoutException:
    print("Bara de căutare nu a fost găsită.")
    driver.quit()
    exit()

try:
    videoLink = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Ed Sheeran - Shape of You"))
    )
    videoLink.click()
    print("Am dat click pe videoclipul dorit.")
except TimeoutException:
    print("Videoclipul nu a fost găsit în rezultate.")
    driver.quit()
    exit()

# Începerea înregistrării video și audio
print("Începerea înregistrării...")

# Parametri pentru PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Inițializează PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
frames = []  # Pentru datele audio

# Setări pentru video
screen_width, screen_height = pyautogui.size()
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output_video.avi", fourcc, 10, (screen_width, screen_height))

start_time = time.time()
while time.time() - start_time <= 120:  # Se asigură că înregistrarea durează exact 2 minute (120 secunde)
    # Înregistrează audio
    data = stream.read(CHUNK)
    frames.append(data)

    # Captură de ecran și scriere în video
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
    out.write(frame)

print("Oprire înregistrare.")

# Încheie înregistrarea audio
stream.stop_stream()
stream.close()
audio.terminate()

# Salvează fișierul audio
with wave.open("output_audio.wav", "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# Eliberare resurse video
out.release()
print("Înregistrare salvată în 'output_video.avi' și 'output_audio.wav'.")

# Închide browserul
driver.quit()
print("Am închis browserul.")
