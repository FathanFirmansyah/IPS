# Cara melakukan plotting data dan pembentukan ruangan
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x1 = 0
y1 = 0

x2 = 2.14
y2 = 3.06

x3 = 5.76
y3 = 3.06

ax.scatter(x1, y1, color='red', label='AP 1')
ax.scatter(x2, y2, color='blue', label='AP 2')
ax.scatter(x3, y3, color='black', label='AP 3')

# Definisikan koordinat titik-titik persegi panjang
# x = [0, 2.90,2.90,0,0]
# y = [0, 0,7.22,7.22,0]

x = [0, 5.76, 5.76, 2.14, 2.14, 0, 0]
y = [0, 0, 5.16, 5.16, 3.06, 3.06, 0]

# Gambar persegi panjang
ax.plot(x, y)

ax.set_xlim(-2, 8)
ax.set_ylim(-2, 8)

# Tampilkan legenda
ax.legend()

# Menambahkan judul
plt.title("Ruang 2")

# Tampilkan gambar
plt.show()
