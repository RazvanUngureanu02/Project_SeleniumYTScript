from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Specifică calea către ChromeDriver
service = Service('C:/Users/2021 august/Desktop/ChromeDriver/chromedriver.exe')

# Inițializează driverul Chrome
driver = webdriver.Chrome(service=service)

# Deschide YouTube
driver.get("https://www.youtube.com")
time.sleep(3)

# Caută un videoclip
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("Python tutorial")  # Înlocuiește cu termenul de căutare dorit
search_box.send_keys(Keys.RETURN)
time.sleep(3)

# Selectează și redă primul videoclip din rezultate
video = driver.find_element(By.ID, "video-title")
video.click()
time.sleep(10)  # Lasă videoclipul să ruleze pentru 10 secunde

# Închide browserul
driver.quit()