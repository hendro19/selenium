import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

def edit_excel(path_excel):
    try:
        # Membaca data dari file Excel
        df = pd.read_excel(path_excel)
        
        print("Data di file Excel:")
        print(df)

        # Menambahkan/menyunting data di Excel
        username = input("Masukkan username baru: ")
        password = input("Masukkan password baru: ")

        # Menambahkan baris baru atau mengedit baris pertama (misalnya)
        df.loc[0] = [username, password]  # Menyunting baris pertama dengan username dan password baru

        # Menyimpan perubahan ke file Excel
        df.to_excel(path_excel, index=False)
        print(f"File Excel berhasil diperbarui: {path_excel}")

    except Exception as e:
        print(f"Terjadi kesalahan saat mengedit file Excel: {e}")

def jalankan_script(path_excel='', url_login=''):
    try:
        # Cek jika file atau URL kosong
        if not path_excel or not url_login:
            print("File Excel atau URL login tidak tersedia. Skrip tidak dapat dijalankan tanpa keduanya.")
            return

        # Membaca data dari file Excel
        df = pd.read_excel(path_excel)

        # Inisialisasi driver Chrome
        driver = webdriver.Chrome()
        driver.get(url_login)
        driver.maximize_window()
        time.sleep(2)  # Tunggu hingga halaman dimuat

        # File untuk mencatat user yang gagal login
        failed_logins = []

        # Loop melalui setiap baris di file Excel dan mencoba login
        for index, row in df.iterrows():
            username = row['Username']  # Mengambil username
            password = row['Password']  # Mengambil password

            # Mencari elemen input username dan password
            username_input = driver.find_element(By.ID, "Editbox1")
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(1)

            password_input = driver.find_element(By.ID, "Editbox2")
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(1)

            # Klik tombol login
            logon_button = driver.find_element(By.ID, "buttonLogOn")
            logon_button.click()
            time.sleep(2)

            # Cek apakah login berhasil atau gagal
            try:
                error_message = driver.find_element(By.ID, "span-credentials-ko")
                if error_message.is_displayed():
                    print(f"Login gagal untuk {username}")
                    failed_logins.append(username)
            except NoSuchElementException:
                print(f"Login berhasil untuk {username}")

                # Logout jika login berhasil
                logout_link = driver.find_element(By.LINK_TEXT, "Keluar")
                logout_link.click()
                time.sleep(2)

            # Kembali ke halaman login
            driver.get(url_login)
            time.sleep(2)

        # Mencatat username yang gagal login ke file
        if failed_logins:
            with open("failed_logins.txt", "w") as file:
                for user in failed_logins:
                    file.write(user + "\n")
            print("Username yang gagal login telah dicatat di 'failed_logins.txt'.")

        driver.quit()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def edit_link_web():
    """Fungsi untuk mengedit URL login"""
    url_login = input("Masukkan URL login baru (biarkan kosong untuk tidak mengubah): ") or ''
    if not url_login:
        print("URL login kosong. Skrip tidak akan berjalan tanpa URL login.")
    else:
        print(f"URL login telah diperbarui menjadi: {url_login}")
    return url_login

def tampilkan_menu():
    path_excel = ''  # Default path kosong
    url_login = ''   # Default URL kosong
    
    while True:
        print("\n=== Menu Program ===")
        print("1. Edit file Excel")
        print("2. Edit URL login web")
        print("3. Jalankan skrip login otomatis")
        print("4. Keluar")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == "1":
            path_excel = input("Masukkan path ke file Excel yang akan diedit (biarkan kosong untuk tidak mengubah): ") or ''
            edit_excel(path_excel)
        elif pilihan == "2":
            url_login = edit_link_web()  # Memanggil fungsi untuk mengedit link
        elif pilihan == "3":
            jalankan_script(path_excel, url_login)
        elif pilihan == "4":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    tampilkan_menu()
