import time
import pywifi
import math
from filterpy.kalman import KalmanFilter
import numpy as np
from multiprocessing import Process, Event

reference_rssi_dict = {
    "RuijieAP1": -31.24,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": -28.80,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": -32.70   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
}

n_dict = {
    "RuijieAP1": 1.75,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": 1.75,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": 1.6   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
}
    
# beacon_positions = {
#     "RuijieAP1": np.array([0, 0]),
#     "RuijieAP2": np.array([0, -6.3]),
#     "RuijieAP3": np.array([5.9, -6.3])
# }

# Inisialisasi Filter Kalman
kf = KalmanFilter(dim_x=1, dim_z=1)
kf.F = np.array([[1.0]])  # Matriks transisi
kf.H = np.array([[1.0]])  # Matriks pengukuran
kf.R = 5  # Kovariansi pengukuran (dalam contoh ini, disesuaikan dengan skala pengukuran)
kf.P = np.eye(1)  # Matriks kovariansi awal (dalam contoh ini, matriks identitas)

def calculate_distanceKalman(rssi, ssid, ssidN, data_count):
    """
    Calculate the distance based on RSSI, reference RSSI (A), and path loss exponent (n).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        A (float): Reference RSSI at 1 meter.
        n (float): Path loss exponent.
    
    Returns:
        float: Distance between transmitter and receiver.
    """
    # Update Filter Kalman dengan pengukuran RSSI
    reference_rssi = reference_rssi_dict[ssid]

    if data_count == 0:
        kf.x = np.array([reference_rssi])
    n = n_dict[ssidN]
    kf.predict()
    kf.update(np.array([rssi]))

    estimated_rssi = kf.x[0]
    distanceKalman = 10 ** ((reference_rssi - estimated_rssi) / (10 * n))
    return distanceKalman

def calculate_distance(RSSI, ssid, ssidN):
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
    n = n_dict[ssidN]
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
    n = -1*(RSSI - A) / (10 * math.log10(d))
    return n

def trilateration(xAP1,yAP1,rAP1,xAP2,yAP2,rAP2,xAP3,yAP3,rAP3):
    """
    Trilateration untuk menentukan posisi pengguna berdasarkan sinyal yang diterima dari beberapa beacon.
    
    Args:
        beacons (list): List koordinat beacon dalam format (x, y).
        distances (list): List jarak antara pengguna dan masing-masing beacon.
    
    Returns:
        tuple: Koordinat perkiraan posisi pengguna dalam format (x, y).
    """
    A = 2*xAP2 - 2*xAP1
    B = 2*yAP2 - 2*yAP1
    C = rAP1**2 - rAP2**2 - xAP1**2 + xAP2**2 - yAP1**2 + yAP2**2
    D = 2*xAP3 - 2*xAP2
    E = 2*yAP3 - 2*yAP2
    F = rAP2**2 - rAP3**2 - xAP2**2 + xAP3**2 - yAP2**2 + yAP3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    return x,y

def scan_wifi_rssi(ssid, outputRSSI, outputJarak, outputKalmanFilter, outputN, max_data, stop_event):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        # Inisialisasi hitungan data yang diambil
        data_count = 0 

        # # Inisialisasi list koordinat beacon
        # beacons = []  
        # # Inisialisasi list jarak
        # distances = [] 

        while data_count < max_data and not stop_event.is_set():
            iface.scan()
            time.sleep(2)
            scan_results = iface.scan_results()

            for result in scan_results:
                if ssid in result.ssid:
                    # Fungsi untuk mendapatkan nilai RSSI
                    rssi = result.signal
                    with open(outputRSSI, "a") as file:
                        file.write(f"RSSI {ssid} = {rssi} dBm\n")
                    print(f"{data_count}.RSSI {ssid} = {rssi} dBm")

                    # Fungsi Calculate Path Loss Exponent
                    # nValue = calculate_path_loss_exponent(rssi,ssid,4.00)
                    # with open(outputN, "a") as file:
                    #     file.write(f"N-{ssid}-4m = {nValue}\n")
                    # print(f"N-{ssid}-4m = {nValue}")

                    # Fungsi untuk mendapatkan nilai jarak TANPA Kalman Filter
                    distance = calculate_distance(rssi, ssid, ssid)
                    with open(outputJarak, "a") as file:
                        file.write(f" Jarak {ssid} = {distance} meter\n")
                    print(f"Jarak {ssid} = {distance} meter")

                    # Fungsi untuk menghitung jarak device ke AP yang sudah menggunakan kalman filter
                    distanceKalman = calculate_distanceKalman(rssi, ssid, ssid, data_count)
                    with open(outputKalmanFilter, "a") as file:
                        file.write(f"KF {ssid} = {distanceKalman:.2f} meter\n")
                    print(f"KF {ssid} = {distanceKalman:.2f} meter")

                    # # Menambahkan posisi beacon sesuai dengan SSID
                    # beacons.append(beacon_positions[ssid])
                    # # Menambah jarak
                    # distances.append(distanceKalman)
                    
                    data_count += 1  # Menambah jumlah data yang diambil
                    
                    if data_count >= max_data:
                        print(f"Pengambilan Data Selesai")
                    break
            else:
                print(f"Tidak dapat menemukan {ssid}")
                stop_event.set()  # Set stop_event jika SSID tidak ditemukan
                break

        # # Jika semua data telah dikumpulkan, lakukan trilaterasi
        # if len(beacons) == max_data:
        #     user_position = trilateration(beacons, distances)
        #     print(f"Posisi perkiraan pengguna untuk SSID {ssid}: {user_position}")

    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")

if __name__ == "__main__":
    target_ssids = ["RuijieAP1","RuijieAP2","RuijieAP3"]  # Ganti dengan daftar SSID yang ingin Anda lacak
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
