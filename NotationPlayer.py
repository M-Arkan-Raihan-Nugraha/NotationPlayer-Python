import numpy as np
import simpleaudio as sa

# Map notasi ke frekuensi
notasi_ke_freq = {
    # Nada rendah (oktaf bawah)
    '1-': 130, '2-': 146, '3-': 164, '4-': 174, '5-': 196, '6-': 220, '7-': 246,
    # Nada standar
    '1': 261, '2': 293, '3': 329, '4': 349, '5': 392, '6': 440, '7': 493,
    # Nada tinggi (oktaf atas)
    '1+': 523, '2+': 587, '3+': 659, '4+': 698, '5+': 784, '6+': 880, '7+': 987
}

def generate_tone(freq, duration=0.4, fs=44100):
    t = np.linspace(0, duration, int(fs * duration), False)
    note = np.sin(freq * t * 2 * np.pi)

    # Fade-in/out 20 ms
    fade_len = int(0.02 * fs)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    note[:fade_len] *= fade_in
    note[-fade_len:] *= fade_out

    # Kurangi amplitudo untuk menghindari noise
    audio = note * (2**14)
    return audio.astype(np.int16)

def main():
    print("Contoh Input Notasi: 1- 2 3 . 4 5+")
    notasi = input("Masukkan Notasi: ").split()

    fs = 44100
    full_song = np.array([], dtype=np.int16)

    for n in notasi:
        freq = notasi_ke_freq.get(n)
        if freq:
            audio = generate_tone(freq)
            full_song = np.concatenate((full_song, audio))
        elif n == '.':
            # Jeda Kata(titik): 0.5 detik
            silence = np.zeros(int(fs * 0.5), dtype=np.int16)
            full_song = np.concatenate((full_song, silence))
        else:
            # Jeda nada(spasi): 0.1 detik
            silence = np.zeros(int(fs * 0.1), dtype=np.int16)
            full_song = np.concatenate((full_song, silence))

    play_obj = sa.play_buffer(full_song, 1, 2, fs)
    play_obj.wait_done()

if __name__ == "__main__":
    main()


# NOT IBU KITA KARTINI
# 1 . 2 3 4 5 . 3 1 . 6 . 1+ 7 6 5 . . . 4 . 6 5 4 3 . 1 . 2 . 4 3 2 1 . . . 4 . 3 4 6 5 6 5 3 1 3 2 3 4 5 3 . . . 4 . 3 4 6 5 6 5 3 1 3 2 4 7- 2 1

# NOT GUNDUL GUNDUL PACUL
# 1 3 . 1 3 4 5 5 7 1+ 7 1+ 7 5 . 1 3 . 1 3 4 5 5 7 1+ 7 1+ 7 5 . 1 . 3 . 5 . 4 4 5 4 3 1 4 3 1 . 1 3 . 5 . 4 4 5 4 3 1 4 3 1

# NOT BINTANG KECIL
# 5 3+ 2+ 1+ . . 7 2+ 1+ 7 6 5 . . . 6 7 1+ 5 . . 1+ 3+ 5+ 3+ 1+ 2+ . . . 5+ 3+ 2+ 1+ . 3+ 5+ 3+ 2+ 1+ 6 . . . 7 1+ 6 5 . 2+ 3+ 4+ 2+ 6 7 1+