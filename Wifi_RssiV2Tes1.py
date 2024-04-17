import time
import pywifi
import math
from filterpy.kalman import KalmanFilter
import numpy as np
from multiprocessing import Process, Event

# Parameter-parameter untuk Model Path Loss
reference_rssi_dict = {
    "RuijieAP1": -26,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": -28,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": -34   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
}

# Path Loss Exponent (biasanya berkisar antara 2.0 hingga 4.0)
n = 2.5

# Inisialisasi Filter Kalman
kf = KalmanFilter(dim_x=1, dim_z=1)
kf.F = np.array([[1.0]])  # Matriks transisi
kf.H = np.array([[1.0]])  # Matriks pengukuran
kf.R = 5  # Kovariansi pengukuran (dalam contoh ini, disesuaikan dengan skala pengukuran)
kf.P = np.eye(1)  # Matriks kovariansi awal (dalam contoh ini, matriks identitas)

def calculate_distanceKalman(rssi, ssid):
    # Update Filter Kalman dengan pengukuran RSSI
    reference_rssi = reference_rssi_dict[ssid]
    kf.x = np.array([reference_rssi])
    kf.predict()
    kf.update(np.array([rssi]))

    estimated_rssi = kf.x[0]
    distanceKalman = 10 ** (reference_rssi - estimated_rssi) / (10 * n)
    return distanceKalman

def calculate_distance(RSSI, ssid, n):
    """
    Calculate the distance based on RSSI, reference RSSI (A), and path loss exponent (n).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        A (float): Reference RSSI at 1 meter.
        n (float): Path loss exponent.
    
    Returns:
        float: Distance between transmitter and receiver.
    """
    A = reference_rssi_dict[ssid]
    d = 10 ** ((A - RSSI) / (10 * n))
    return d

def calculate_path_loss_exponent(RSSI, ssid, d):
    """
    Calculate the path loss exponent (n) based on RSSI, reference RSSI (A), and distance (d).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        A (float): Reference RSSI at 1 meter.
        d (float): Distance between transmitter and receiver.
    
    Returns:
        float: Path loss exponent (n).
    """
    A = reference_rssi_dict[ssid]
    n = -(RSSI - A) / (10 * math.log10(d))
    return n

def scan_wifi_rssi(ssid, outputRSSI, outputJarak, outputKalmanFilter, outputN, max_data, stop_event):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        data_count = 0  # Inisialisasi hitungan data yang diambil
        while data_count < max_data and not stop_event.is_set():
            iface.scan()
            time.sleep(2)
            scan_results = iface.scan_results()

            for result in scan_results:
                if ssid in result.ssid:
                    # Fungsi untuk mendapatkan nilai RSSI
                    rssi = result.signal
                    with open(outputRSSI, "a") as file:
                        file.write(f"{ssid}= {rssi} dBm\n")

                    # Fungsi untuk mendapatkan nilai jarak TANPA Kalman Filter
                    # distance = calculate_distance(rssi, ssid, n)
                    # with open(outputJarak, "a") as file:
                    #     file.write(f"{ssid}= {distance} meter\n")

                    # Fungsi untuk menghitung jarak device ke AP yang sudah menggunakan kalman filter
                    # distanceKalman = calculate_distanceKalman(rssi, ssid)
                    # with open(outputKalmanFilter, "a") as file:
                    #     file.write(f"KF= {distanceKalman:.2f} meter\n")
                    # print(f"{ssid}: RSSI={rssi} dBm, Jarak={distanceKalman:.2f} meter")

                    # Fungsi Calculate Path Loss Exponent
                    nValue = calculate_path_loss_exponent(rssi,ssid,2.00)
                    with open(outputN, "a") as file:
                        file.write(f"N-{ssid}= {nValue} dBm\n")
                    print(f"N:{nValue}, {ssid}")
                    
                    data_count += 1  # Menambah jumlah data yang diambil
                    
                    if data_count >= max_data:
                        print(f"Pengambilan Data Selesai")
                    break
            else:
                print(f"Tidak dapat menemukan {ssid}")
                stop_event.set()  # Set stop_event jika SSID tidak ditemukan
                break

    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")

if __name__ == "__main__":
    target_ssids = ["RuijieAP1"]  # Ganti dengan daftar SSID yang ingin Anda lacak
    max_data = 100

    # Event untuk menghentikan proses jika SSID tidak ditemukan
    stop_event = Event()

    processes = []
    for ssid in target_ssids:
        outputRSSI = f"outputRSSI_{ssid}.txt"
        outputJarak = f"outputJarak_{ssid}.txt"
        outputKalmanFilter = f"outputKF_{ssid}.txt"
        outputN = f"outputN_{ssid}.txt"
        process = Process(target=scan_wifi_rssi, args=(ssid, outputRSSI, outputJarak, outputKalmanFilter, outputN, max_data, stop_event))
        processes.append(process)
        process.start()

    # Tunggu proses selesai
    for process in processes:
        process.join()

    # Cek apakah SSID tidak ditemukan
    if stop_event.is_set():
        print("Scanning dihentikan karena salah satu SSID tidak ditemukan.")
