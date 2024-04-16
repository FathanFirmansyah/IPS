import time
import pywifi
import math
from filterpy.kalman import KalmanFilter
import numpy as np
from multiprocessing import Process, Event

# Parameter-parameter untuk Model Path Loss
reference_rssi_dict = {
    "RuijieAP1": -28,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": -30,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": -26   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
}
n = 2.5  # Path Loss Exponent (biasanya berkisar antara 2.0 hingga 4.0)

# Inisialisasi Filter Kalman
kf = KalmanFilter(dim_x=1, dim_z=1)
kf.F = np.array([[1.0]])  # Matriks transisi
kf.H = np.array([[1.0]])  # Matriks pengukuran
kf.R = 5  # Kovariansi pengukuran (dalam contoh ini, disesuaikan dengan skala pengukuran)
kf.P = np.eye(1)  # Matriks kovariansi awal (dalam contoh ini, matriks identitas)

def calculate_distanceKalman(rssi, ssid):
    # Ambil referensi RSSI untuk SSID tertentu
    reference_rssi = reference_rssi_dict[ssid]
    
    # Update Filter Kalman dengan pengukuran RSSI
    kf.x = np.array([reference_rssi])  # Inisialisasi nilai RSSI awal
    kf.predict()
    kf.update(np.array([rssi]))
    estimated_rssi = kf.x[0]
    
    ratio = (reference_rssi - estimated_rssi) / (10 * n)
    distanceKalman = 10 ** ratio
    return distanceKalman

def trilaterate(beacons, distances):
    """
    Trilateration untuk menentukan posisi pengguna berdasarkan sinyal yang diterima dari beberapa beacon.
    
    Args:
        beacons (list): List koordinat beacon dalam format (x, y).
        distances (list): List jarak antara pengguna dan masing-masing beacon.
    
    Returns:
        tuple: Koordinat perkiraan posisi pengguna dalam format (x, y).
    """
    num_beacons = len(beacons)
    
    # Konversi ke numpy array
    beacons = np.array(beacons)
    distances = np.array(distances)
    
    # Inisialisasi matriks A dan vektor b
    A = 2 * (beacons[1:] - beacons[0])
    b = np.square(distances[1:]) - np.square(distances[0])
    
    # Hitung perkiraan posisi pengguna
    x = np.linalg.solve(A.T.dot(A), A.T.dot(b))
    
    # Tambahkan koordinat beacon pertama
    user_position = x + beacons[0]
    
    return tuple(user_position)

def scan_wifi_rssi(ssid, outputRSSI, outputKalmanFilter, max_data, stop_event):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        data_count = 0  # Inisialisasi hitungan data yang diambil
        
        beacons = []  # Inisialisasi list koordinat beacon
        distances = []  # Inisialisasi list jarak
        
        while data_count < max_data and not stop_event.is_set():
            iface.scan()
            time.sleep(2)
            scan_results = iface.scan_results()

            for result in scan_results:
                if ssid in result.ssid:
                    rssi = result.signal
                    distanceKalman = calculate_distanceKalman(rssi, ssid)  # Pass ssid to the function
                    with open(outputRSSI, "a") as file:
                        file.write(f"{ssid}: RSSI={rssi} dBm\n")
                    with open(outputKalmanFilter, "a") as file:
                        file.write(f"KalmanFilter={distanceKalman:.2f} meter\n")
                    print(f"{ssid}: RSSI={rssi} dBm, Jarak={distanceKalman:.2f} meter")
                    
                    data_count += 1  # Menambah jumlah data yang diambil
                    
                    beacons.append(result.pos)  # Menambah koordinat beacon
                    distances.append(distanceKalman)  # Menambah jarak

                    if data_count >= max_data:
                        print(f"Pengambilan Data Selesai")
                    break
            else:
                print(f"Tidak dapat menemukan {ssid}")
                stop_event.set()  # Set stop_event jika SSID tidak ditemukan
                break

        # Jika semua data telah dikumpulkan, lakukan trilaterasi
        if len(beacons) == max_data:
            user_position = trilaterate(beacons, distances)
            print(f"Posisi perkiraan pengguna untuk SSID {ssid}: {user_position}")
    
    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")

if __name__ == "__main__":
    target_ssids = ["RuijieAP1", "RuijieAP2","RuijieAP3"]  # Ganti dengan daftar SSID yang ingin Anda lacak
    max_data = 30

    # Event untuk menghentikan proses jika SSID tidak ditemukan
    stop_event = Event()

    processes = []
    for ssid in target_ssids:
        outputRSSI = f"outputRSSI_{ssid}.txt"
        outputKalmanFilter = f"outputKF_{ssid}.txt"
        process = Process(target=scan_wifi_rssi, args=(ssid, outputRSSI, outputKalmanFilter, max_data, stop_event))
        processes.append(process)
        process.start()

    # Tunggu proses selesai
    for process in processes:
        process.join()

    # Cek apakah SSID tidak ditemukan
    if stop_event.is_set():
        print("Scanning dihentikan karena salah satu SSID tidak ditemukan.")
