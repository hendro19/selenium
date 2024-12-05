import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.service import Service
import time
import os

# Path ke geckodriver
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

url = "https://minahasa.siskeudes.link/"
driver.get(url)
driver.maximize_window()

failed_logins = []
no_apk_users = []

# Fungsi untuk menunggu elemen
def wait_for_element(by, value, timeout=5):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except NoSuchElementException:
        print(f"Elemen dengan XPath '{value}' tidak ditemukan.")
        return None  # Kembalikan None jika elemen tidak ditemukan
    except TimeoutException:
        print(f"Timeout: Elemen dengan XPath '{value}' tidak muncul dalam {timeout} detik.")
        return None  # Kembalikan None jika waktu habis

# Tentukan nama folder di mana file akan disimpan
folder_name = "logs"

# Cek apakah folder sudah ada, jika tidak, buat folder tersebut
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Folder '{folder_name}' berhasil dibuat.")

# Loop untuk setiap baris data di Excel
for index, row in df.iterrows():
    username = row['Username']
    password = row['Password']

    # Login ke halaman
    username_input = driver.find_element(By.ID, "Editbox1")
    username_input.clear()
    username_input.send_keys(username)
    time.sleep(1)

    password_input = driver.find_element(By.ID, "Editbox2")
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(1)

    logon_button = driver.find_element(By.ID, "buttonLogOn")
    logon_button.click()
    time.sleep(1)

    try:
        error_message = driver.find_element(By.ID, "span-credentials-ko")
        if error_message.is_displayed():
            print(f"Login gagal usr {username}")
            failed_logins.append(username)
            continue  # Langsung lanjut ke user berikutnya
    except NoSuchElementException:
        print(f"Login berhasil usr {username}")

        # Tunggu hingga elemen aplikasi muncul selama 5 detik
        time.sleep(2)

        # Tunggu elemen dengan ID 'apps' sebelum mencari aplikasi "Tahun 2024"
        # apps_container = wait_for_element(By.ID, "apps", timeout=5)  # Timeout 5 detik
        # if apps_container:
        #     try:
        #         # Mencari aplikasi "Tahun 2024" dalam elemen #apps
        #         app_element = wait_for_element(By.XPATH, "//div[@id='apps']//span[text()='Tahun 2024']", timeout=5)  # Timeout 5 detik
        #         if not app_element:
        #             print(f"Aplikasi Siskeudes tidak ditemukan untuk {username}")
        #             no_apk_users.append(username)  # Mencatat pengguna yang tidak menemukan aplikasi
        #         else:
        #             print(f"Aplikasi Siskeudes ditemukan untuk {username}")  # Debugging
        #     except TimeoutException:
        #         # print(f"Timeout: Aplikasi Siskeudes tidak ditemukan untuk {username}")
        #         no_apk_users.append(username)  # Mencatat pengguna yang tidak menemukan aplikasi
        # else:
        #     print(f"Elemen #apps tidak ditemukan untuk {username}")
        #     no_apk_users.append(username)

        # Tunggu elemen dengan ID 'apps' sebelum mencari siskeudes"
        apps_container = wait_for_element(By.ID, "apps", timeout=2)
        if apps_container:
            try:
                # Mencari aplikasi "Tahun 2024" dalam elemen #apps
                app_element = wait_for_element(By.XPATH, "//div[@id='apps']//span[text()='Tahun 2024']", timeout=2)
                if not app_element:
                    print(f"Aplikasi Siskeudes tidak ditemukan usr  {username}")
                    no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi
            except TimeoutException:
                # print(f"Timeout: Aplikasi 'Siskeudes' tidak ditemukan untuk {username}")
                no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi
        else:
            print(f"Elemen #apps tidak ditemukan usr {username}")
            no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi

        # Logout setelah selesai
        logout_link = driver.find_element(By.LINK_TEXT, "Keluar")
        logout_link.click()
        time.sleep(1)  # Tunggu sebentar setelah logout

    # Kembali ke halaman login
    driver.get(url)
    time.sleep(1)

# Mencatat username yang gagal login ke file di dalam folder logs
if failed_logins:
    with open(os.path.join(folder_name, "failed_logins.txt"), "w") as file:
        for user in failed_logins:
            file.write(user + "\n")
    print(f"Username yang gagal login telah dicatat di '{folder_name}/failed_logins.txt'.")

# Mencatat username yang tidak menemukan aplikasi ke file di dalam folder logs
if no_apk_users:
    with open(os.path.join(folder_name, "no_apk_users.txt"), "w") as file:
        for user in no_apk_users:
            file.write(user + "\n")
    print(f"Username yang tidak menemukan apk Siskeudes telah dicatat di '{folder_name}/no_apk_users.txt'.")

# Tutup browser setelah pengujian selesai
driver.quit()
