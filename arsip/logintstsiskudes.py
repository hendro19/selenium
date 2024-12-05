import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.service import Service
import time

GECKO_DRIVER_PATH = 'C:\\geckodriver-v0.35.0-win64\\geckodriver.exe'

# Membaca data dari file Excel
df = pd.read_excel('excel/minahasa.xlsx')  # Ganti dengan path ke file Excel Anda

# Jika file Excel kosong, hentikan eksekusi
if df.empty:
    print("File Excel kosong. Program dihentikan.")
    exit()

# Inisialisasi driver Firefox menggunakan Service
service = Service(GECKO_DRIVER_PATH)
driver = webdriver.Firefox(service=service)

# URL halaman login
url = "https://minahasa.siskeudes.link/"  # Sesuaikan dengan URL login yang sesuai
driver.get(url)
driver.maximize_window()

# File untuk mencatat user yang gagal login dan tidak menemukan aplikasi
failed_logins = []
no_apk_users = []

# Fungsi untuk menunggu elemen
def wait_for_element(by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except (NoSuchElementException, TimeoutException):
        return None

# Loop melalui setiap baris di file Excel dan mencoba login
for index, row in df.iterrows():
    username = row['Username']  # Mengambil username
    password = row['Password']  # Mengambil password

    # 1. Mencari elemen username (input text)
    try:
        username_input = driver.find_element(By.ID, "Editbox1")  # Sesuaikan ID elemen
        username_input.clear()
        username_input.send_keys(username)
    except NoSuchElementException:
        print(f"Elemen username tidak ditemukan untuk {username}")
        failed_logins.append(username)
        continue

    # 2. Mencari elemen password (input password)
    try:
        password_input = driver.find_element(By.ID, "Editbox2")  # Sesuaikan ID elemen
        password_input.clear()
        password_input.send_keys(password)
    except NoSuchElementException:
        print(f"Elemen password tidak ditemukan untuk {username}")
        failed_logins.append(username)
        continue

    # 3. Mencari tombol login dan klik
    try:
        logon_button = driver.find_element(By.ID, "buttonLogOn")  # Sesuaikan ID tombol login
        logon_button.click()
    except NoSuchElementException:
        print(f"Tombol login tidak ditemukan untuk {username}")
        failed_logins.append(username)
        continue
    
    time.sleep(2)

    # Cek apakah login berhasil atau gagal
    try:
        # Memeriksa jika elemen untuk pesan kesalahan login ada
        error_message = driver.find_element(By.ID, "span-credentials-ko")
        if error_message.is_displayed():
            print(f"Login gagal untuk {username}")
            failed_logins.append(username)  # Menambahkan username yang gagal login ke daftar
            continue  # Lanjutkan ke user berikutnya
    except NoSuchElementException:
        # Jika elemen "span-credentials-ko" tidak ditemukan, login dianggap berhasil
        print(f"Login berhasil untuk {username}")

        # Mencari aplikasi 'Tahun 2024' dalam div #apps
        try:
            app_element = wait_for_element(By.XPATH, "//div[@id='apps']//span[text()='Tahun 2024']")
            if not app_element:
                app_element = wait_for_element(By.XPATH, "//*[@id='apps']/div")
            if not app_element:
                print(f"Aplikasi 'Tahun 2024' tidak ditemukan untuk {username}")
                no_apk_users.append(username)
            # else:
                # print(f"Aplikasi 'Tahun 2024' ditemukan untuk {username}")
        except Exception as e:
            print(f"Terjadi kesalahan saat mencari aplikasi untuk {username}: {e}")
            no_apk_users.append(username)

        # Logout menggunakan link text "Keluar"
        try:
            logout_link = driver.find_element(By.LINK_TEXT, "Keluar")
            logout_link.click()
        except NoSuchElementException:
            print(f"Link logout tidak ditemukan untuk {username}")
        
        time.sleep(1)  # Tunggu sebentar setelah logout

    # Kembali ke halaman login jika diperlukan
    driver.get(url)
    time.sleep(1)

# Mencatat username yang gagal login ke file
if failed_logins:
    with open("failed_logins.txt", "w") as file:
        for user in failed_logins:
            file.write(user + "\n")
    print(f"Username yang gagal login telah dicatat di 'failed_logins.txt'.")

# Mencatat username yang tidak menemukan aplikasi ke file
if no_apk_users:
    with open("no_apk_users.txt", "w") as file:
        for user in no_apk_users:
            file.write(user + "\n")
    print(f"Username yang tidak menemukan aplikasi 'Tahun 2024' telah dicatat di 'no_apk_users.txt'.")

# Tutup browser setelah pengujian selesai
driver.quit()
