# Cara melakukan plotting data dan pembentukan ruangan
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x1 = 2.84
y1 = 2.58

x2 = 2.73
y2 = 2.51

x3 = 2.52
y3 = 2.68

x4 = 1.51
y4 = 4.12

x5 = 2.19
y5 = 3.30

ax.scatter(x1, y1, color='red', label='Prediksi 1 Data')
ax.scatter(x2, y2, color='blue', label='Prediksi 10 Data')
ax.scatter(x3, y3, color='black', label='Prediksi 20 Data')
ax.scatter(x4, y4, color='purple', label='Prediksi 40 Data')
ax.scatter(x5, y5, color='orange', label='Prediksi 80 Data')

# Definisikan koordinat titik-titik persegi panjang
x = [0, 5.76, 5.76, 2.15, 2.15, 0, 0]
y = [0, 0, 5.16, 5.16, 3.06, 3.06, 0]

# Tambahkan titik pada koordinat asli (0, 1.53)
ax.scatter(3.94, 4.09, color='green', label='Asli')

# Gambar persegi panjang
ax.plot(x, y)

ax.set_xlim(-5, 10)
ax.set_ylim(-5, 10)

# Tampilkan legenda
ax.legend()

# Tampilkan gambar
plt.show()
