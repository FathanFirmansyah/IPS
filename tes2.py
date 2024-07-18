# Menghitung nilai peningkatan akurasi error sebelum dan sesudah kalman filter
# Nilai error sebelum dan sesudah menggunakan filter Kalman
error_sebelum = 2.05
error_sesudah = 1.99

# Menghitung peningkatan akurasi
peningkatan_akurasi = ((error_sebelum - error_sesudah) / error_sebelum) * 100

# Membulatkan hasil ke dua angka di belakang koma
peningkatan_akurasi = round(peningkatan_akurasi, 2)

print(f"Peningkatan akurasi: {peningkatan_akurasi}%")
