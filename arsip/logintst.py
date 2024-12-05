from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

# Inisialisasi WebDriver dengan ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def open_login_page():
    """Buka halaman login"""
    driver.get("https://practicetestautomation.com/practice-test-login/")
    time.sleep(2)

def login(username, password):
    """Masukkan username, password dan klik tombol login"""
    # Temukan elemen input username dan password
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)

    # Klik tombol login
    driver.find_element(By.ID, "submit").click()
    time.sleep(2)

def verify_text_present(expected_text):
    """Verifikasi apakah teks yang diharapkan ada di halaman"""
    body_text = driver.find_element(By.TAG_NAME, "body").text
    return expected_text in body_text

def verify_error_message(expected_message):
    """Verifikasi pesan error"""
    try:
        error_message = driver.find_element(By.ID, "error").text
        return error_message == expected_message
    except NoSuchElementException:
        return False

# Test Case 1: Positive LogIn Test
print("\nTest Case 1: Positive LogIn Test")
open_login_page()
login("student", "Password123")

# Verifikasi URL setelah login berhasil
if "practicetestautomation.com/logged-in-successfully/" in driver.current_url:
    print("✅ URL berhasil diverifikasi.")
else:
    print("❌ URL tidak sesuai.")

# Verifikasi teks di halaman
if verify_text_present("Congratulations") or verify_text_present("successfully logged in"):
    print("✅ Teks halaman berhasil diverifikasi.")
else:
    print("❌ Teks halaman tidak ditemukan.")

# Verifikasi tombol Log Out
try:
    logout_button = driver.find_element(By.LINK_TEXT, "Log out")
    if logout_button.is_displayed():
        print("✅ Tombol Log out ditemukan.")
    else:
        print("❌ Tombol Log out tidak ditemukan.")
except NoSuchElementException:
    print("❌ Tombol Log out tidak ada.")

# Logout sebelum melanjutkan ke test case berikutnya
logout_button.click()
time.sleep(2)

# Test Case 2: Negative Username Test
print("\nTest Case 2: Negative Username Test")
open_login_page()
login("incorrectUser", "Password123")

if verify_error_message("Your username is invalid!"):
    print("✅ Pesan error username berhasil diverifikasi.")
else:
    print("❌ Pesan error username tidak sesuai.")

# Test Case 3: Negative Password Test
print("\nTest Case 3: Negative Password Test")
open_login_page()
login("student", "incorrectPassword")

if verify_error_message("Your password is invalid!"):
    print("✅ Pesan error password berhasil diverifikasi.")
else:
    print("❌ Pesan error password tidak sesuai.")

# Tutup browser setelah semua test selesai
driver.quit()
