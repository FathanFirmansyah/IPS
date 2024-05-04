import signal
import sys

def signal_handler(sig, frame):
    print("\n----------------EXIT----------------")
    sys.exit(0)

# Penanganan sinyal SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

try:
    from pywifi import PyWiFi, const
    import time
    import pywifi
    import math
    from math import sin, cos, sqrt, atan2, radians, pi
    from filterpy.kalman import KalmanFilter
    import numpy as np
    from multiprocessing import Process, Event, Manager, Lock
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import csv
    import pandas as pd
except ImportError as e:
    print("Modul yang diperlukan belum diinstal:", e)
    print("Silakan instal modul yang diperlukan dengan menggunakan pip.")
    exit(1)

reference_rssi_dict = {
    "RuijieAP1": -29,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": -25,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": -23,   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
}

n_dict = {
    "RuijieAP1": 3.21,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": 2.83,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": 3.82,   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
}
    
beacon_positions = {
    "RuijieAP1": np.array([0, 0]),
    "RuijieAP2": np.array([5.76, 0]),
    "RuijieAP3": np.array([5.76, 5.16])
}

# Inisialisasi Filter Kalman
kfAP1 = KalmanFilter(dim_x=1, dim_z=1)
kfAP1.F = np.array([[1.0]])  # Matriks transisi
kfAP1.H = np.array([[1.0]])  # Matriks pengukuran
kfAP1.R = 5  # Kovariansi pengukuran (dalam contoh ini, disesuaikan dengan skala pengukuran)
kfAP1.P = np.eye(1)  # Matriks kovariansi awal (dalam contoh ini, matriks identitas)

kfAP2 = KalmanFilter(dim_x=1, dim_z=1)
kfAP2.F = np.array([[1.0]])  # Matriks transisi
kfAP2.H = np.array([[1.0]])  # Matriks pengukuran
kfAP2.R = 5  # Kovariansi pengukuran (dalam contoh ini, disesuaikan dengan skala pengukuran)
kfAP2.P = np.eye(1)  # Matriks kovariansi awal (dalam contoh ini, matriks identitas)

kfAP3 = KalmanFilter(dim_x=1, dim_z=1)
kfAP3.F = np.array([[1.0]])  # Matriks transisi
kfAP3.H = np.array([[1.0]])  # Matriks pengukuran
kfAP3.R = 5  # Kovariansi pengukuran (dalam contoh ini, disesuaikan dengan skala pengukuran)
kfAP3.P = np.eye(1)  # Matriks kovariansi awal (dalam contoh ini, matriks identitas)
def calculate_distanceKalmanAP1(rssi, ssid, ssidN, data_count):
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
        kfAP1.x = np.array([reference_rssi])
    kfAP1.predict()
    kfAP1.update(np.array([rssi]))

    estimated_rssi = kfAP1.x[0]
    distanceKalman = 10 ** ((reference_rssi - estimated_rssi) / (10 * n))
    return distanceKalman

def calculate_distanceKalmanAP2(rssi, ssid, ssidN, data_count):
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
        kfAP2.x = np.array([reference_rssi])
    kfAP2.predict()
    kfAP2.update(np.array([rssi]))

    estimated_rssi = kfAP2.x[0]
    distanceKalman = 10 ** ((reference_rssi - estimated_rssi) / (10 * n))
    return distanceKalman

def calculate_distanceKalmanAP3(rssi, ssid, ssidN, data_count):
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
        kfAP3.x = np.array([reference_rssi])
    kfAP3.predict()
    kfAP3.update(np.array([rssi]))

    estimated_rssi = kfAP3.x[0]
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

def ambilDataKF(ssid,lock,outputTrilaterasiKF,kolom):
    data = pd.read_csv('outputKF.csv')
    AP1 = data[ssid[0]]
    AP2 = data[ssid[1]]
    AP3 = data[ssid[2]]

    meanAP1 = np.nanmean(AP1)
    print(f"Rata-Rata Jarak {ssid[0]} ke titik:",meanAP1)
    meanAP2 = np.nanmean(AP2)
    print(f"Rata-Rata Jarak {ssid[1]} ke titik:", meanAP2)
    meanAP3 = np.nanmean(AP3)
    print(f"Rata-Rata Jarak {ssid[2]} ke titik:", meanAP3)

    x,y = trilateration(ssid[0],meanAP1,ssid[1],meanAP2,ssid[2],meanAP3)
    print("Trilaterasi Kalman(x,y)=",x,y)

    with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
        with open(outputTrilaterasiKF, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=kolom)
            info = {
                "x": x,
                "y": y
            }
            csv_writer.writerow(info)

def ambilData(ssid,lock,outputTrilaterasi,kolom):
    data = pd.read_csv('outputJarak.csv')
    AP1 = data[ssid[0]]
    AP2 = data[ssid[1]]
    AP3 = data[ssid[2]]

    meanAP1 = np.nanmean(AP1)
    meanAP2 = np.nanmean(AP2)
    meanAP3 = np.nanmean(AP3)

    x,y = trilateration(ssid[0],meanAP1,ssid[1],meanAP2,ssid[2],meanAP3)
    print("Kalkulasi Tanpa Kalman (x,y)=",x,y)

    with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
        with open(outputTrilaterasi, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=kolom)
            info = {
                "x": x,
                "y": y
            }
            csv_writer.writerow(info)

def scan_location(ssid, outputRSSI, outputJarak, outputKalmanFilter, max_data, stop_event, result_dict, lock, outputTrilaterasiKF,kolom,outputTrilaterasi):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        # Inisialisasi hitungan data yang diambil
        data_count = 0
        AP1 = ssid[0]
        AP2 = ssid[1]
        AP3 = ssid[2]

        countAP1 = 0
        countAP2 = 0
        countAP3 = 0

        countKFAP1=0
        countKFAP2=0
        countKFAP3=0
        while data_count <= max_data and not stop_event.is_set():
            # Menambah jumlah data yang diambil
            data_count += 1
            iface.scan()
            time.sleep(1)
            scan_results = iface.scan_results()
            countAP1 = 0
            countAP2 = 0
            countAP3 = 0
            print("========================================================================")
            for result in scan_results:
                if countAP1 == 0:
                    if AP1 in result.ssid:
                        countAP1 += 1
                        # Fungsi untuk mendapatkan nilai RSSI
                        rssi = result.signal
                        with open(outputRSSI, "a") as file:
                            file.write(f"RSSI {AP1} = {rssi} dBm\n")
                        print(f"{data_count}.RSSI {AP1} = {rssi} dBm")

                        # Fungsi untuk mendapatkan nilai jarak TANPA Kalman Filter
                        distanceAP1 = calculate_distance(rssi, AP1, AP1)
                        print(f"Jarak {AP1} = {distanceAP1} meter")

                        # Fungsi untuk menghitung jarak device ke AP yang sudah menggunakan kalman filter
                        distanceKalmanAP1 = calculate_distanceKalmanAP1(rssi, AP1, AP1, countKFAP1)
                        print(f"Jarak KF {AP1} = {distanceKalmanAP1} meter")
                        
                        countKFAP1 +=1
                if countAP2 == 0:
                    if AP2 in result.ssid:
                        countAP2 +=1
                        # Fungsi untuk mendapatkan nilai RSSI
                        rssi = result.signal
                        with open(outputRSSI, "a") as file:
                            file.write(f"RSSI {AP2} = {rssi} dBm\n")
                        print(f"{data_count}.RSSI {AP2} = {rssi} dBm")

                        # Fungsi untuk mendapatkan nilai jarak TANPA Kalman Filter
                        distanceAP2 = calculate_distance(rssi, AP2, AP2)
                        print(f"Jarak {AP2} = {distanceAP2} meter")

                        # Fungsi untuk menghitung jarak device ke AP yang sudah menggunakan kalman filter
                        distanceKalmanAP2 = calculate_distanceKalmanAP2(rssi, AP2, AP2, countKFAP2)
                        print(f"Jarak KF {AP2} = {distanceKalmanAP2} meter")
                        
                        countKFAP2 +=1
                if countAP3 == 0:
                    if AP3 in result.ssid:
                        countAP3 +=1
                        # Fungsi untuk mendapatkan nilai RSSI
                        rssi = result.signal
                        with open(outputRSSI, "a") as file:
                            file.write(f"RSSI {AP3} = {rssi} dBm\n")
                        print(f"{data_count}.RSSI {AP3} = {rssi} dBm")

                        # Fungsi untuk mendapatkan nilai jarak TANPA Kalman Filter
                        distanceAP3 = calculate_distance(rssi, AP3, AP3)
                        print(f"Jarak {AP3} = {distanceAP3} meter")

                        # Fungsi untuk menghitung jarak device ke AP yang sudah menggunakan kalman filter
                        distanceKalmanAP3 = calculate_distanceKalmanAP3(rssi, AP3, AP3, countKFAP3)
                        print(f"Jarak KF {AP3} = {distanceKalmanAP3} meter")
                        
                        countKFAP3 +=1
            for AP in ssid:
                if countAP1 == 0:
                    print(f"AP {AP1} Tidak Ditemukan")
                    exit()
                if countAP2 == 0:
                    print(f"AP {AP2} Tidak Ditemukan")
                    exit()
                if countAP3 == 0:
                    print(f"AP {AP3} Tidak Ditemukan")
                    exit()
            if countAP1 == 1 and countAP2 == 1 and countAP3 ==1:
                with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
                    with open(outputKalmanFilter, 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=target_ssids)
                        info = {
                            "RuijieAP1": distanceKalmanAP1,
                            "RuijieAP2": distanceKalmanAP2,
                            "RuijieAP3": distanceKalmanAP3
                        }
                        csv_writer.writerow(info)
                        print(f"AP1:{distanceKalmanAP1}, AP2:{distanceKalmanAP2}, AP3:{distanceKalmanAP3}")
                with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
                    with open(outputJarak, 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=target_ssids)
                        info = {
                            "RuijieAP1": distanceAP1,
                            "RuijieAP2": distanceAP2,
                            "RuijieAP3": distanceAP3
                        }
                        csv_writer.writerow(info)
                ambilDataKF(ssid,lock,outputTrilaterasiKF,kolom)
                ambilData(ssid,lock,outputTrilaterasi,kolom)
            if countAP1 == 1 and countAP2 == 1 and countAP3 == 1 and data_count >= max_data:
                print(f"Pengambilan Data Selesai")
                exit()    
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
                        file.write(f"N-{ssid}-{jarak}m = {nValue}\n")
                    print(f"N-{ssid}-{jarak}m = {nValue}")
                    
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

def scan_distance(ssid, outputRSSI, outputJarak, max_data, stop_event):
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

                    # Fungsi untuk mendapatkan nilai jarak TANPA Kalman Filter
                    distance = calculate_distance(rssi, ssid, ssid)
                    with open(outputJarak, "a") as file:
                        file.write(f" Jarak {ssid} = {distance} meter\n")
                    print(f"Jarak {ssid} = {distance} meter")
                    
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
    target_ssids = ["RuijieAP1","RuijieAP2","RuijieAP3"]
    max_data = 1000000000000
    # Event untuk menghentikan proses jika SSID tidak ditemukan
    stop_event = Event()
    manager = Manager()
    # Membuat dictionary untuk result jarak
    result_dict = manager.dict()
    # Dictionary untuk menyimpan array berdasarkan SSID
    array_dict = {}
    processes = []
    # Inisialisasi objek Lock
    lock = Lock()

    print("Daftar Pilihan:")
    print("1. Mencari Titik Lokasi (+Kalman Filter)")
    print("2. Mencari Nilai N (Path Loss Exponent)")
    print("3. Mencari Nilai RSSI")
    print("4. Mencari Nilai Jarak ke 1 AP")

    pilihan = float(input("Masukkan Pilihan Anda: "))

    kolom = ["x","y"]
    if pilihan == 1:
        lock = Lock()

        outputKalmanFilter = f"outputKF.csv"
        with open(outputKalmanFilter, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=target_ssids)
            csv_writer.writeheader()
        
        outputTrilaterasiKF = f"outputTrilaterasiKF.csv"
        with open(outputTrilaterasiKF, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=kolom)
            csv_writer.writeheader()

        outputJarak = f"outputJarak.csv"
        with open(outputJarak, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=target_ssids)
            csv_writer.writeheader()
        
        outputTrilaterasi = f"outputTrilaterasi.csv"
        with open(outputTrilaterasi, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=kolom)
            csv_writer.writeheader()
        
        outputRSSI = f"outputRSSI.csv"

        scan_location(target_ssids,outputRSSI,outputJarak,outputKalmanFilter,max_data,stop_event,result_dict,lock,outputTrilaterasiKF,kolom,outputTrilaterasi)


    elif pilihan == 2:
        jarak = float(input("Masukkan Jarak Lokasi ke AP: "))
        for ssid in target_ssids:
            outputRSSI = f"outputRSSI_{ssid}_{jarak}m.txt"
            outputN = f"outputN_{ssid}_{jarak}m.txt"
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

    elif pilihan == 4:
        for ssid in target_ssids:
            outputRSSI = f"outputRSSI_{ssid}.txt"
            outputJarak = f"outputJarak_{ssid}.txt"
            process = Process(target=scan_distance, args=(ssid, outputRSSI, outputJarak, max_data, stop_event))
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