# Cara melakukan plotting data dan pembentukan ruangan
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
    
# Ruang 1, Posisi 1
x1 = 0
y1 = 0
x2 = 5.76
y2 = 0
x3 = 5.76
y3 = 5.16

    # Ruang 1, Posisi 2
# x1 = 0
# y1 = 0
# x2 = 2.14
# y2 = 3.06
# x3 = 5.76
# y3 = 3.06

    # 
# x1 = 2.90
# y1 = 0
# x2 = 1.45
# y2 = 3.61
# x3 = 1.45
# y3 = 7.22

    # Titik Asli
x4 = 0
y4 = 1.53

    # Titik +KF
x5 = 2.52
y5 = 2.68
    # Titik -KF
x6 = 2.41
y6 = 2.72


ax.scatter(x1, y1, color='red', label='AP 1')
ax.scatter(x2, y2, color='blue', label='AP 2')
ax.scatter(x3, y3, color='black', label='AP 3')
ax.scatter(x4, y4, color='green', label='Asli')
ax.scatter(x5, y5, color='purple', label='Prediksi +KF')
ax.scatter(x6, y6, color='yellow', label='Prediksi -KF')

# koordinat titik-titik Ruang 1
x = [0, 5.76, 5.76, 2.14, 2.14, 0, 0]
y = [0, 0, 5.16, 5.16, 3.06, 3.06, 0]

# koordinat titik-titik Ruang 2
# x = [0, 2.90,2.90,0,0]
# y = [0, 0,7.22,7.22,0]


# Gambar Ruang
ax.plot(x, y)

ax.set_xlim(-2, 8)
ax.set_ylim(-2, 8)

# Tampilkan legenda
ax.legend()

# Menambahkan judul
plt.title("Ruang 1")

# Tampilkan gambar
plt.show()
