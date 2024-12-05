from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Setup opsi untuk Firefox dalam mode headless
options = Options()
options.headless = True  # Menjalankan Firefox tanpa tampilan GUI

# Tentukan path ke geckodriver menggunakan Service
service = Service(executable_path='C:\\geckodriver-v0.35.0-win64\\geckodriver.exe')

# Inisialisasi webdriver dengan service dan opsi headless
driver = webdriver.Firefox(service=service, options=options)

# Arahkan ke halaman yang ingin diambil screenshot-nya
driver.get("https://www.google.com")

# Ambil screenshot dan simpan ke file
driver.save_screenshot("screenshot.png")

# Menutup browser setelah selesai
driver.quit()
