import time
import pywifi
import math
from filterpy.kalman import KalmanFilter
import numpy as np

# Parameter-parameter untuk Model Path Loss
reference_rssi = -29  # RSSI pada jarak referensi (dalam dBm)
n = 2.0  # Path Loss Exponent (biasanya berkisar antara 2.0 hingga 4.0)

# Inisialisasi Filter Kalman
kf = KalmanFilter(dim_x=1, dim_z=1)
kf.x = np.array([reference_rssi])  # Inisialisasi nilai RSSI awal
kf.F = np.array([[1.0]])  # Matriks transisi
kf.H = np.array([[1.0]])  # Matriks pengukuran

def calculate_distanceKalman(rssi):
    # Update Filter Kalman dengan pengukuran RSSI
    kf.predict()
    kf.update(np.array([rssi]))
    estimated_rssi = kf.x[0]
    
    ratio = (reference_rssi - estimated_rssi) / (10 * n)
    distanceKalman = 10 ** ratio
    return distanceKalman

def calculate_distance(rssi):
    ratio = (reference_rssi-rssi) / (10 *n)
    distance = 10 ** ratio
    return distance

def scan_wifi_rssi(ssid, outputRSSI, outputNonFilter, outputKalmanFilter, max_data):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    data_count = 0  # Inisialisasi hitungan data yang diambil
    try:
        while data_count < max_data:
            iface.scan()
            time.sleep(2)
            scan_results = iface.scan_results()

            for result in scan_results:
                if ssid in result.ssid:
                    rssi = result.signal
                    distance = calculate_distance(rssi)
                    distanceKalman = calculate_distanceKalman(rssi)
                    with open(outputRSSI, "a") as file:
                        file.write(f"RSSI= {rssi} dBm\n")
                    with open(outputNonFilter, "a") as file:
                        file.write(f"NonFilter= {distance:.2f} meter\n")
                    with open(outputKalmanFilter, "a") as file:
                        file.write(f"KalmanFilter= {distanceKalman:.2f} meter\n")
                    print(f"{ssid}: RSSI= {rssi} dBm, Jarak= {distanceKalman:.2f} meter")

                    data_count += 1  # Menambah jumlah data yang diambil

                    if data_count >= max_data:
                        print(f"Pengambilan Data Selesai")
                    break

                else:
                    print(f"Tidak dapat menemukan {ssid}")
                time.sleep(2)  # Interval cek setiap 2 detik
    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")

if __name__ == "__main__":
    target_ssid = "Ruijie"
    outputRSSI = "outputRSSI2.txt"  # Ganti dengan nama file yang Anda inginkan
    outputNonFilter = "outputNF2.txt"  # Ganti dengan nama file yang Anda inginkan
    outputKalmanFilter = "outputKF2.txt"  # Ganti dengan nama file yang Anda inginkan

    max_data = 30

    try:
        scan_wifi_rssi(target_ssid, outputRSSI, outputNonFilter, outputKalmanFilter, max_data)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
