from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

driver_path = 'C:\\geckodriver-v0.35.0-win64\\geckodriver.exe' # Contoh: "C:/path_to_geckodriver/geckodriver.exe"

# Setup Firefox untuk mode headless
  # Menjalankan Firefox dalam mode headless

# Tentukan Service untuk geckodriver
service = Service(executable_path=driver_path)

# Inisialisasi WebDriver untuk Firefox dengan Service dan opsi headless
driver = webdriver.Firefox()

try:
    # Step 1: Buka halaman login e-learning STTKD
    login_url = 'https://elearning.sttkd.ac.id/login/index.php'
    driver.get(login_url)
    time.sleep(2)  # Tunggu halaman dimuat

    # Step 2: Klik tombol "Google (Email STTKD)"
    google_login_button = driver.find_element(By.CSS_SELECTOR, 'a.btn.login-identityprovider-btn')
    google_login_button.click()
    time.sleep(2)  # Tunggu halaman Google Login terbuka

    # Step 3: Masukkan email di halaman Google
    email_input = driver.find_element(By.ID, 'identifierId')
    email_input.send_keys('190809366@students.sttkd.ac.id')  # Ganti dengan email STTKD Anda
    email_input.send_keys(Keys.ENTER)
    time.sleep(1)  # Tunggu halaman untuk password

    # Step 4: Masukkan password di halaman Google
    password_input = driver.find_element(By.NAME, 'Passwd')
    password_input.send_keys('qwerty123!@#')  # Ganti dengan password Anda
    password_input.send_keys(Keys.ENTER)
    time.sleep(2)  # Tunggu proses login

    # Step 5: Tunggu redirect kembali ke e-learning
    time.sleep(5)

    # Verifikasi apakah login berhasil dengan memeriksa teks "Dashboard"
    if "Dashboard" in driver.page_source:
        print("Login berhasil!")
    else:
        print("Login gagal atau membutuhkan verifikasi tambahan.")

finally:
    # Tutup browser
    driver.quit()
