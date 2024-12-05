import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Membaca data dari file Excel
df = pd.read_excel('test.xlsx')  # Ganti dengan path ke file Excel Anda

# Ganti dengan path ke ChromeDriver Anda
#driver_path = 'C:\chromedriver-win64'
driver = webdriver.Chrome()

# URL halaman login
url = "https://siskeudes-rohilkab.id/"  # Ganti dengan URL login yang sesuai
driver.get(url)
driver.maximize_window()
time.sleep(2)  # Tunggu sampai halaman dimuat

# File untuk mencatat user yang gagal login
failed_logins = []

# Loop melalui setiap baris di file Excel dan mencoba login
for index, row in df.iterrows():
    username = row['Username']  # Mengambil username
    password = row['Password']  # Mengambil password

    # 1. Mencari elemen username (input text)
    username_input = driver.find_element(By.ID, "Editbox1")  # Menggunakan ID
    username_input.clear()  # Membersihkan kolom sebelum mengetik
    username_input.send_keys(username)  # Isi username yang diambil dari Excel
    time.sleep(1)

    # 2. Mencari elemen password (input password)
    password_input = driver.find_element(By.ID, "Editbox2")  # Menggunakan ID
    password_input.clear()  # Membersihkan kolom sebelum mengetik
    password_input.send_keys(password)  # Isi password yang diambil dari Excel
    time.sleep(1)

    # 3. Mencari tombol login dan klik (input button)
    logon_button = driver.find_element(By.ID, "buttonLogOn")
    logon_button.click()  # Klik tombol "Masuk"
    time.sleep(2)

    # Cek apakah login berhasil
    try:
        # Misalnya, setelah login berhasil, kita bisa memeriksa keberadaan elemen tertentu di dashboard
        dashboard_element = driver.find_element(By.ID, "dashboard")  # Misalkan ada elemen dashboard setelah login
        print(f"Login berhasil untuk {username}")
    except:
        print(f"Login gagal untuk {username}")
        failed_logins.append(username)  # Menambahkan username yang gagal login ke daftar

    # Untuk membersihkan kolom login agar siap untuk login berikutnya
    username_input.clear()
    password_input.clear()
    time.sleep(1)

# Mencatat username yang gagal login ke file
if failed_logins:
    with open("failed_logins.txt", "w") as file:
        for user in failed_logins:
            file.write(user + "\n")
    print(f"Username yang gagal login telah dicatat di 'failed_logins.txt'.")
else:
    print("Semua pengguna berhasil login.")

# Tutup browser setelah pengujian selesai
driver.quit()
