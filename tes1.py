import time
import pywifi
import math
from filterpy.kalman import KalmanFilter
import numpy as np

# Parameter-parameter untuk Model Path Loss
reference_rssi = -30  # RSSI pada jarak referensi (dalam dBm)
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

def scan_wifi_rssi(ssid, outputRSSI, outputNonFilter, outputKalmanFilter):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        while True:
            iface.scan()
            time.sleep(2)
            scan_results = iface.scan_results()

            for result in scan_results:
                if ssid in result.ssid:
                    rssi = result.signal
                    distance= calculate_distance(rssi)
                    distanceKalman = calculate_distanceKalman(rssi)
                    with open(outputRSSI, "a") as file:
                        file.write(f"{ssid}: RSSI={rssi} dBm\n")
                    with open(outputNonFilter, "a") as file:
                        file.write(f"NonFilter={distance:.2f} meter\n")
                    with open(outputKalmanFilter, "a") as file:
                        file.write(f"KalmanFilter={distanceKalman:.2f} meter\n")
                    print(f"{ssid}: RSSI={rssi} dBm, Jarak={distanceKalman:.2f} meter")
                    break
            else:
                print(f"Tidak dapat menemukan {ssid}")
            time.sleep(2)  # Interval cek setiap 3 detik
    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")

if __name__ == "__main__":
    target_ssid = input("Masukkan nama SSID jaringan WiFi yang ingin Anda monitor: ")
    outputRSSI = "outputRSSI1.txt"  # Ganti dengan nama file yang Anda inginkan
    outputNonFilter = "outputNF1.txt"  # Ganti dengan nama file yang Anda inginkan
    outputKalmanFilter = "outputKF1.txt"  # Ganti dengan nama file yang Anda inginkan

    try:
        scan_wifi_rssi(target_ssid, outputRSSI, outputNonFilter, outputKalmanFilter)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
