from filterpy.kalman import KalmanFilter
import numpy as np

# Buat objek KalmanFilter
kf = KalmanFilter(dim_x=1, dim_z=1)

# Definisikan matriks state transition (A) dan matriks pengukuran (H)
kf.F = np.array([[1.0]])  # Matriks state transition 

kf.H = np.array([[1.0]]) # Matriks pengukuran

# Definisikan matriks kovariansi proses (Q) dan kovariansi pengukuran (R)
kf.Q *= 0.01  # Matriks kovariansi proses (dalam contoh ini, nilai kecil untuk proses yang stabil)
kf.R = 5  # Kovariansi pengukuran (dalam contoh ini, disesuaikan dengan skala pengukuran)

# Data set offline (misalnya, pengukuran jarak)
data_set = [-41, -41, -42, -42, -43, -43, -43, -41, -41, -44, -44,
    -44, -43, -43, -43, -44, -44, -38, -38, -38, -40, -40,
    -41, -41, -41, -40, -40, -40, -40, -40]  # Data set awal yang bisa diubah nilainya

# Inisialisasi state dan kovariansi awal
kf.x = np.array([-29])  # Nilai awal state (misalnya, nilai pertama dari data set)
kf.P = np.eye(1)  # Matriks kovariansi awal (dalam contoh ini, matriks identitas)

# Proses Kalman Filter
for measurement in data_set:
    # Prediksi
    kf.predict()

    # Update dengan pengukuran aktual
    kf.update(measurement)

    ratio = (-29 - kf.x[0]) / (10 * 2.0)
    distanceKalman = 10 ** ratio

    print(f"{distanceKalman:.2f}")
    # Tampilkan hasil estimasi jarak
    # print("Jarak:", kf.x[0][0])
