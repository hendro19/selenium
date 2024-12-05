import time
import sys

# Lirik lagu disimpan dalam daftar untuk mempermudah pengaturan tempo per baris
lyrics = [
    "When you lose something you cannot replace",  # Baris 1
    "Tears stream down your face, and I",          # Baris 2
    "Tears stream down your face",                 # Baris 3
    "I promise you, I will learn from my mistakes" # Baris 4
]

# Fungsi untuk efek mengetik
def typing_effect(text, char_delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(char_delay)
    print()  # Untuk membuat baris baru setelah selesai

# Menampilkan lirik dengan efek mengetik sesuai tempo
def play_lyrics_with_tempo(lyrics, line_delays):
    for i, line in enumerate(lyrics):
        typing_effect(line, char_delay=0.05)  # Efek mengetik untuk setiap baris
        time.sleep(line_delays[i])  # Jeda setelah baris selesai (sesuai tempo)

# Jeda antar baris berdasarkan tempo Fix You (dalam detik)
line_delays = [3.5, 4.0, 3.0, 5.0]

# Memainkan lirik dengan tempo
play_lyrics_with_tempo(lyrics, line_delays)
