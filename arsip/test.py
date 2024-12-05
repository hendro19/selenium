from selenium import webdriver

# Membuat instance WebDriver
driver = webdriver.Chrome()  # Jika Anda menggunakan Firefox, ganti dengan webdriver.Firefox()

# Akses URL
driver.get("https://www.google.com")

# Tunggu beberapa detik agar halaman bisa dimuat
driver.implicitly_wait(5)

# Ambil judul halaman
print(driver.title)

# Tutup browser
driver.quit()
