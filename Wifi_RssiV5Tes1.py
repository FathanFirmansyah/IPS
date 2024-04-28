import time
import pywifi
import math
from math import sin, cos, sqrt, atan2, radians, pi
from filterpy.kalman import KalmanFilter
import numpy as np
from multiprocessing import Process, Event, Manager

reference_rssi_dict = {
    "RuijieAP1": -31.24,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": -28.80,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": -32.70,   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
}

n_dict = {
    "RuijieAP1": 1.75,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": 1.75,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": 1.6,   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
}
    
beacon_positions = {
    "RuijieAP1": np.array([0, 0]),
    "RuijieAP2": np.array([0, -6.3]),
    "RuijieAP3": np.array([5.9, -6.3])
}

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
    n = n_dict[ssidN]
    if data_count == 0:
        kf.x = np.array([reference_rssi])
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

def trilateration(ssid1,rAP1,ssid2,rAP2,ssid3,rAP3):
    """
    Trilateration untuk menentukan posisi pengguna berdasarkan sinyal yang diterima dari beberapa beacon.
    
    Args:
        beacons (list): List koordinat beacon dalam format (x, y).
        distances (list): List jarak antara pengguna dan masing-masing beacon.
    
    Returns:
        tuple: Koordinat perkiraan posisi pengguna dalam format (x, y).
    """
    xAP1 = beacon_positions[ssid1][0]
    yAP1 = beacon_positions[ssid1][1]
    xAP2 = beacon_positions[ssid2][0]
    yAP2 = beacon_positions[ssid2][1]
    xAP3 = beacon_positions[ssid3][0]
    yAP3 = beacon_positions[ssid3][1]

    A = 2*xAP2 - 2*xAP1
    B = 2*yAP2 - 2*yAP1
    C = rAP1**2 - rAP2**2 - xAP1**2 + xAP2**2 - yAP1**2 + yAP2**2
    D = 2*xAP3 - 2*xAP2
    E = 2*yAP3 - 2*yAP2
    F = rAP2**2 - rAP3**2 - xAP2**2 + xAP3**2 - yAP2**2 + yAP3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    return x,y

def scan_location(ssid, outputRSSI, outputJarak, outputKalmanFilter, max_data, stop_event, result_dict):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        # Inisialisasi hitungan data yang diambil
        data_count = 0 
        distances = [] 

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
                    print(f"{data_count+1}.RSSI {ssid} = {rssi} dBm")

                    # Fungsi untuk mendapatkan nilai jarak TANPA Kalman Filter
                    distance = calculate_distance(rssi, ssid, 1.6)
                    with open(outputJarak, "a") as file:
                        file.write(f" Jarak {ssid} = {distance} meter\n")
                    print(f"Jarak {ssid} = {distance} meter")

                    # Fungsi untuk menghitung jarak device ke AP yang sudah menggunakan kalman filter
                    distanceKalman = calculate_distanceKalman(rssi, ssid, ssid, data_count)
                    with open(outputKalmanFilter, "a") as file:
                        file.write(f"KF {ssid} = {distanceKalman:.4f} meter\n")
                    print(f"KF {ssid} = {distanceKalman:.4f} meter")

                    distances.append(distanceKalman)
                    
                    # Menambah jumlah data yang diambil
                    data_count += 1  
                    
                    if data_count >= max_data:
                        print(f"Pengambilan Data {ssid} Selesai")
                    break
            else:
                print(f"Tidak dapat menemukan {ssid}")
                # Set stop_event jika SSID tidak ditemukan
                stop_event.set()  
                break
        
        # Memasukkan nilai distances ke dalam dict dengan kunci SSID
        result_dict[ssid] = distances  
    
    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")

def scan_N(ssid, outputRSSI, outputN, max_data, stop_event, jarak):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        # Inisialisasi hitungan data yang diambil
        data_count = 0

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
                    print(f"{data_count+1}.RSSI {ssid} = {rssi} dBm")

                    # Fungsi Calculate Path Loss Exponent
                    nValue = calculate_path_loss_exponent(rssi,ssid,jarak)
                    with open(outputN, "a") as file:
                        file.write(f"N-{ssid}-4m = {nValue}\n")
                    print(f"N-{ssid}-4m = {nValue}")
                    
                    data_count += 1  # Menambah jumlah data yang diambil
                    
                    if data_count >= max_data:
                        print(f"Pengambilan Data {ssid} Selesai")
                    break
            else:
                print(f"Tidak dapat menemukan {ssid}")
                stop_event.set()  # Set stop_event jika SSID tidak ditemukan
                break
    
    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")

def scan_rssi(ssid, outputRSSI, max_data, stop_event):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        # Inisialisasi hitungan data yang diambil
        data_count = 0

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
                    print(f"{data_count+1}.RSSI {ssid} = {rssi} dBm")
                    
                    # Menambah jumlah data yang diambil
                    data_count += 1  
                    
                    if data_count >= max_data:
                        print(f"Pengambilan Data {ssid} Selesai")
                    break
            else:
                print(f"Tidak dapat menemukan {ssid}")
                # Set stop_event jika SSID tidak ditemukan
                stop_event.set()  
                break
    
    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")


if __name__ == "__main__":
    # Ganti dengan daftar SSID yang ingin Anda lacak
    target_ssids = ["RuijieAP1", "RuijieAP2", "RuijieAP3"]
    max_data = 3

    # Event untuk menghentikan proses jika SSID tidak ditemukan
    stop_event = Event()
    manager = Manager()
    # Membuat dictionary untuk result jarak
    result_dict = manager.dict()
    # Dictionary untuk menyimpan array berdasarkan SSID
    array_dict = {}
    processes = []

    print("Daftar Pilihan:")
    print("1. Mencari Titik Lokasi (+Kalman Filter)")
    print("2. Mencari Nilai N (Path Loss Exponent)")
    print("3. Mencari Nilai RSSI")

    pilihan = float(input("Masukkan Pilihan Anda: "))

    if pilihan == 1:
        for ssid in target_ssids:
            outputRSSI = f"outputRSSI_{ssid}.txt"
            outputJarak = f"outputJarak_{ssid}.txt"
            outputKalmanFilter = f"outputKF_{ssid}.txt"
            process = Process(target=scan_location, args=(ssid, outputRSSI, outputJarak, outputKalmanFilter, max_data, stop_event, result_dict))
            processes.append(process)
            process.start()

        # Tunggu proses selesai
        for process in processes:
            process.join()

        # Cek apakah SSID tidak ditemukan
        if stop_event.is_set():
            print("Scanning dihentikan karena salah satu SSID tidak ditemukan.")

        AP1 : any
        AP2 : any
        AP3 : any
        no = 0
        # Mengakses hasil untuk setiap SSID dari result_dict
        for ssid in target_ssids:
            distances = result_dict.get(ssid, [])  # Menggunakan get() untuk mengatasi SSID yang tidak ditemukan
            array_dict[ssid] = []

            for  x in distances:
                array_dict[ssid]=np.append(array_dict[ssid],x)
            
            if no == 0:
                AP1 = np.nanmean(array_dict[ssid])
                print(f"Rata-Rata Jarak {ssid} ke titik:", AP1)
                no+=1
            elif no == 1:
                AP2 = np.nanmean(array_dict[ssid])
                print(f"Rata-Rata Jarak {ssid} ke titik:", AP2)
                no+=1
            elif no == 2:
                AP3 = np.nanmean(array_dict[ssid])
                print(f"Rata-Rata Jarak {ssid} ke titik:", AP3)
                no+=1
        
        x,y = trilateration(target_ssids[0],AP1,target_ssids[1],AP2,target_ssids[2],AP3)
        print("calculated cordinates of tag (x,y)=",x,y)

        # Menghitung jarak prediksi dengan titik sebenarnya
        def calculateDistance(x1,y1,x2,y2):  
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
            return dist
        print("distance between calculated and setup coordinates=", calculateDistance(0, 1.92, x, y) ) 
    
    elif pilihan == 2:
        jarak = float(input("Masukkan Jarak Lokasi ke AP: "))
        for ssid in target_ssids:
            outputRSSI = f"outputRSSI_{ssid}.txt"
            outputN = f"outputN_{ssid}.txt"
            process = Process(target=scan_N, args=(ssid, outputRSSI, outputN, max_data, stop_event, jarak))
            processes.append(process)
            process.start()

        # Tunggu proses selesai
        for process in processes:
            process.join()

        # Cek apakah SSID tidak ditemukan
        if stop_event.is_set():
            print("Scanning dihentikan karena salah satu SSID tidak ditemukan.")
    
    elif pilihan == 3:
        for ssid in target_ssids:
            outputRSSI = f"outputRSSI_{ssid}.txt"
            process = Process(target=scan_rssi, args=(ssid, outputRSSI, max_data, stop_event))
            processes.append(process)
            process.start()

        # Tunggu proses selesai
        for process in processes:
            process.join()

        # Cek apakah SSID tidak ditemukan
        if stop_event.is_set():
            print("Scanning dihentikan karena salah satu SSID tidak ditemukan.")
    
    else:
        exit()