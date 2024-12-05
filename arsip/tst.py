from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Tentukan path ke geckodriver (ganti dengan path Anda sendiri)
driver_path = 'C:\\geckodriver-v0.35.0-win64\\geckodriver.exe' # Contoh: "C:/path_to_geckodriver/geckodriver.exe"

# Setup Firefox untuk mode headless
firefox_options = Options()
firefox_options.add_argument("--headless")  # Menjalankan Firefox dalam mode headless

# Tentukan Service untuk geckodriver
service = Service(executable_path=driver_path)

# Inisialisasi WebDriver untuk Firefox dengan Service dan opsi headless
driver = webdriver.Firefox(service=service, options=firefox_options)

# Buka halaman yang ingin di-screenshot
driver.get("https://www.google.com")

# Tunggu beberapa detik untuk memastikan halaman dimuat
time.sleep(2)

# Ambil screenshot dan simpan ke file
screenshot_path = "google_screenshot_firefox.png"
driver.get_screenshot_as_file(screenshot_path)

print(f"Screenshot berhasil disimpan di: {screenshot_path}")

# Tutup browser setelah selesai
driver.quit()
