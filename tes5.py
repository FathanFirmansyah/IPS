# Mengadopsi fungsi tes3,tes,tes4 untuk kondisi statis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# Fungsi Trilateration
def trilateration(ssid1, rAP1, ssid2, rAP2, ssid3, rAP3):
    xAP1, yAP1 = beacon_positions[ssid1]
    xAP2, yAP2 = beacon_positions[ssid2]
    xAP3, yAP3 = beacon_positions[ssid3]

    A = 2 * xAP2 - 2 * xAP1
    B = 2 * yAP2 - 2 * yAP1
    C = rAP1**2 - rAP2**2 - xAP1**2 + xAP2**2 - yAP1**2 + yAP2**2
    D = 2 * xAP3 - 2 * xAP2
    E = 2 * yAP3 - 2 * yAP2
    F = rAP2**2 - rAP3**2 - xAP2**2 + xAP3**2 - yAP2**2 + yAP3**2
    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)
    return round(x, 2), round(y, 2)

# Fungsi untuk membaca dan memproses file CSV
def read_and_process_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        meanAP1 = df['RuijieAP1'].dropna().mean()
        meanAP2 = df['RuijieAP2'].dropna().mean()
        meanAP3 = df['RuijieAP3'].dropna().mean()
        return meanAP1, meanAP2, meanAP3
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None, None

# Fungsi menghitung jarak Euclidean
def hitung_jarak_euclidean(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)

# # Koordinat titik pengujian pertama
titikX1, titikY1 = 0, 1.53

# # Koordinat titik pengujian kedua
# titikX1, titikY1 = 2.14, 1.53

# # Koordinat titik pengujian ketiga
# titikX1, titikY1 = 3.94, 1.53

# Koordinat titik pengujian keempat
# titikX1, titikY1 = 3.94, 4.09

# Ruang 1, Posisi 1
beacon_positions = {
    "RuijieAP1": [0, 0],
    "RuijieAP2": [5.76, 0],
    "RuijieAP3": [5.76, 5.16]
}

# # Ruang 1, Posisi 2
# beacon_positions = {
#     "RuijieAP1": [0, 0],
#     "RuijieAP2": [2.14, 3.06],
#     "RuijieAP3": [5.76, 3.06]
# }

# # Ruang 2, Posisi 1
# beacon_positions = {
#     "RuijieAP1": [2.90, 0],
#     "RuijieAP2": [0, 3.61],
#     "RuijieAP3": [2.90, 7.22]
# }

# # Ruang 2, Posisi 2
# beacon_positions = {
#     "RuijieAP1": [2.90, 0],
#     "RuijieAP2": [1.45, 3.61],
#     "RuijieAP3": [1.45, 7.22]
# }

# Koordinat Ruang 1
x_coords = [0, 5.76, 5.76, 2.14, 2.14, 0, 0]
y_coords = [0, 0, 5.16, 5.16, 3.06, 3.06, 0]

# # Koordinat Ruang 2
# x_coords = [0, 2.90, 2.90, 0, 0]
# y_coords = [0, 0, 7.22, 7.22, 0]

# Membaca data dari file CSV
meanAP1minKF, meanAP2minKF, meanAP3minKF = read_and_process_csv('Data Penelitian/Data Final v4/Statis/3. Ambil Data tiap Titik/Titik 1/4/outputJarak.csv')
meanAP1plusKF, meanAP2plusKF, meanAP3plusKF = read_and_process_csv('Data Penelitian/Data Final v4/Statis/3. Ambil Data tiap Titik/Titik 1/4/outputKF.csv')

# Menghitung dan menampilkan hasil trilaterasi dan error
if meanAP1minKF and meanAP2minKF and meanAP3minKF:
    TrilaterasiXminKF, TrilaterasiYminKF = trilateration("RuijieAP1", meanAP1minKF, "RuijieAP2", meanAP2minKF, "RuijieAP3", meanAP3minKF)
    error_minKF = hitung_jarak_euclidean(titikX1, titikY1, TrilaterasiXminKF, TrilaterasiYminKF)
    print("Trilaterasi(-KF)(x,y):", TrilaterasiXminKF, ',', TrilaterasiYminKF, "Error:", error_minKF)
else:
    TrilaterasiXminKF, TrilaterasiYminKF, error_minKF = None, None, None

if meanAP1plusKF and meanAP2plusKF and meanAP3plusKF:
    TrilaterasiXplusKF, TrilaterasiYplusKF = trilateration("RuijieAP1", meanAP1plusKF, "RuijieAP2", meanAP2plusKF, "RuijieAP3", meanAP3plusKF)
    error_plusKF = hitung_jarak_euclidean(titikX1, titikY1, TrilaterasiXplusKF, TrilaterasiYplusKF)
    print("Trilaterasi(+KF)(x,y):", TrilaterasiXplusKF, ',', TrilaterasiYplusKF, "Error:", error_plusKF)
else:
    TrilaterasiXplusKF, TrilaterasiYplusKF, error_plusKF = None, None, None

# Plotting
fig, ax = plt.subplots()

# Definisi titik-titik
points = {
    'AP 1': (*beacon_positions['RuijieAP1'], 'red'),
    'AP 2': (*beacon_positions['RuijieAP2'], 'blue'),
    'AP 3': (*beacon_positions['RuijieAP3'], 'black'),
    'Asli': (titikX1, titikY1, 'green')
}

if TrilaterasiXplusKF is not None and TrilaterasiYplusKF is not None:
    points['Prediksi +KF'] = (TrilaterasiXplusKF, TrilaterasiYplusKF, 'purple')
if TrilaterasiXminKF is not None and TrilaterasiYminKF is not None:
    points['Prediksi -KF'] = (TrilaterasiXminKF, TrilaterasiYminKF, 'yellow')

# Plot setiap titik
for label, (x, y, color) in points.items():
    ax.scatter(x, y, color=color, label=label)

# Gambar Ruang
ax.plot(x_coords, y_coords)

# Tampilkan legenda
ax.legend()

# Menambahkan judul
plt.title("Ruang 1")

# Tampilkan gambar
plt.show()
