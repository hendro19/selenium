import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
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
def wait_for_element(by, value, timeout=2):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except NoSuchElementException:
        return None

# Loop melalui setiap baris di file Excel dan mencoba login
for index, row in df.iterrows():
    username = row['Username']  # Mengambil username
    password = row['Password']  # Mengambil password

    # 1. Mencari elemen username (input text)
    username_input = driver.find_element(By.ID, "Editbox1")  # Sesuaikan ID elemen
    username_input.clear()
    username_input.send_keys(username)
    time.sleep(1)

    # 2. Mencari elemen password (input password)
    password_input = driver.find_element(By.ID, "Editbox2")  # Sesuaikan ID elemen
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(1)

    # 3. Mencari tombol login dan klik
    logon_button = driver.find_element(By.ID, "buttonLogOn")  # Sesuaikan ID tombol login
    logon_button.click()
    time.sleep(1)

    # Cek apakah login berhasil atau gagal
    try:
        # Memeriksa jika elemen untuk pesan kesalahan login ada
        error_message = driver.find_element(By.ID, "span-credentials-ko")
        if error_message.is_displayed():
            print(f"Login gagal usr {username}")
            failed_logins.append(username)  # Menambahkan username yang gagal login ke daftar
    except NoSuchElementException:
        # Jika elemen "span-credentials-ko" tidak ditemukan, login dianggap berhasil
        print(f"Login berhasil usr {username}")

        # Menunggu 5 detik sebelum melanjutkan
        time.sleep(2)

        # Mencari aplikasi "Siskeudes" dalam elemen
        # try:
        #     # Mencari div dengan id 'apps' yang berisi aplikasi
        #     app_element = wait_for_element(By.XPATH, "//div[@id='apps']//span[text()='Tahun 2024']")
            
        #     # Memeriksa apakah aplikasi ditemukan
        #     if app_element and app_element.is_displayed():
        #         # Skip print jika aplikasi ditemukan
        #         pass
        #     else:
        #         print(f"Aplikasi 'Siskeudes' tidak ditemukan untuk {username}")
        #         no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi
        # except NoSuchElementException:
        #     # Jika elemen dengan teks 'Tahun 2024' tidak ditemukan
        #     print(f"Aplikasi 'Siskeudes' tidak ditemukan untuk {username}")
        #     no_apk_users.append(username)  
        # Mencatat username yang tidak menemukan aplikasi

        # Mencari aplikasi dengan teks 'Tahun 2024' di dalam div #apps
        try:
                app_element = wait_for_element(By.XPATH, "//div[@id='apps']//span[text()='Tahun 2024']")
                if app_element:
                    # print(f"Aplikasi 'Tahun 2024' ditemukan untuk {username}")
                    pass
                # else:
                #     app_element = wait_for_element(By.XPATH, "//*[@id='apps']/div")
                #     print(f"Aplikasi 'Tahun 2024' tidak ditemukan untuk {username}")
                #     no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi
        except NoSuchElementException:
                    print(f"Aplikasi 'Tahun 2024' tidak ditemukan untuk {username}")
                    no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi

        # try:
        #       # Tunggu hingga elemen 'Tahun 2024' di bagian aplikasi muncul
        #     app_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[@id='apps']//span[text()='Tahun 2024']"))
        #     )
            
        # except TimeoutException:
        #     print("Elemen aplikasi tidak ditemukan")



        # Logout menggunakan link text "Keluar"

        logout_link = driver.find_element(By.LINK_TEXT, "Keluar")
        logout_link.click()
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
    print(f"Username yang tidak menemukan apk 'Siskeudes' telah dicatat di 'no_apk_users.txt'.")


# Tutup browser setelah pengujian selesai
driver.quit()
