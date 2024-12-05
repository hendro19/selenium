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
#df = pd.read_excel('excel\minahasa.xlsx')  # Ganti dengan path ke file Excel Anda
df = pd.read_excel(r'excel\minahasa.xlsx')

# Jika file Excel kosong, hentikan eksekusi
if df.empty:
    print("File Excel kosong. Program dihentikan.")
    exit()

# Inisialisasi driver Firefox menggunakan Service
service = Service(GECKO_DRIVER_PATH)
driver = webdriver.Firefox(service=service)

# Menambahkan waktu tunggu implicit global (10 detik)
# driver.implicitly_wait(10)  # Tunggu hingga 10 detik untuk elemen yang muncul

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
        print(f"Elemen dengan XPath '{value}' tidak ditemukan.")
        return None  # Kembalikan None jika elemen tidak ditemukan
    except TimeoutException:
        print(f"Timeout: Elemen dengan XPath '{value}' tidak muncul dalam {timeout} detik.")
        return None  # Kembalikan None jika waktu habis

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
            continue  # Langsung lanjut ke user berikutnya
    except NoSuchElementException:
        # Jika elemen "span-credentials-ko" tidak ditemukan, login dianggap berhasil
        print(f"Login berhasil usr {username}")

        # Menunggu 5 detik sebelum melanjutkan
        time.sleep(2)

        # Tunggu elemen dengan ID 'apps' sebelum mencari aplikasi "Tahun 2024"
        apps_container = wait_for_element(By.ID, "apps", timeout=2)
        if apps_container:
            try:
                # Mencari aplikasi "Tahun 2024" dalam elemen #apps
                app_element = wait_for_element(By.XPATH, "//div[@id='apps']//span[text()='Tahun 2024']", timeout=2)
                if not app_element:
                    print(f"Aplikasi Siskeudes tidak ditemukan untuk {username}")
                    no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi
            except TimeoutException:
                # print(f"Timeout: Aplikasi 'Siskeudes' tidak ditemukan untuk {username}")
                no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi
        else:
            print(f"Elemen #apps tidak ditemukan untuk {username}")
            no_apk_users.append(username)  # Mencatat username yang tidak menemukan aplikasi

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
    print(f"Username yang tidak menemukan Sikeudes telah dicatat di 'no_apk_users.txt'.")

# Tutup browser setelah pengujian selesai
driver.quit()
