import signal
import sys
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from math import sqrt
from multiprocessing import Lock
import csv


def signal_handler(sig, frame):
    print("\n----------------EXIT----------------")
    sys.exit(0)

def minDistance(A, B, E):
    AB = [B[0] - A[0], B[1] - A[1]]
    BE = [E[0] - B[0], E[1] - B[1]]
    AE = [E[0] - A[0], E[1] - A[1]]

    AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1]

    reqAns = 0

    if AB_BE > 0:
        reqAns = sqrt(BE[0] * BE[0] + BE[1] * BE[1])
    elif AB_AE < 0:
        reqAns = sqrt(AE[0] * AE[0] + AE[1] * AE[1])
    else:
        reqAns = abs(AB[0] * AE[1] - AB[1] * AE[0]) / sqrt(AB[0] * AB[0] + AB[1] * AB[1])

    return reqAns

def animate(i):
    try:
        dataKF = pd.read_csv('outputTrilaterasiKF.csv')
        data = pd.read_csv('outputTrilaterasi.csv')
        # Inisialisasi objek Lock
        lock = Lock()
        fieldnames = ["error"]
        if not dataKF.empty and not data.empty:
            xKF = dataKF['x']
            yKF = dataKF['y']

            x = data['x']
            y = data['y']

            plt.cla()

            # # Gambar Ruang 1
            # plt.plot([0, 5.76, 5.76, 2.14, 2.14, 0, 0], [0, 0, 5.16, 5.16, 3.06, 3.06, 0])
            # Gambar Ruang 2
            plt.plot([0, 2.90, 2.90, 0, 0], [0, 0, 7.22, 7.22, 0])

            # # AP Ruang 1 Posisi 1
            # plt.scatter(0, 0, label = "AP1", color = 'orange')
            # plt.scatter(5.76, 0, label = "AP2", color = 'yellow')
            # plt.scatter(5.76, 5.16, label = "AP3", color = 'purple') 

            # # AP Ruang 1 Posisi 2
            # plt.scatter(0, 0, label = "AP1", color = 'orange')
            # plt.scatter(2.14, 3.06, label = "AP2", color = 'yellow')
            # plt.scatter(5.76, 3.06, label = "AP3", color = 'purple') 

            # # AP Ruang 2 Posisi 1
            # plt.scatter(2.90, 0, label = "AP1", color = 'orange')
            # plt.scatter(0, 3.61, label = "AP2", color = 'yellow')
            # plt.scatter(2.90, 7.22, label = "AP3", color = 'purple') 

            # AP Ruang 2 Posisi 2
            plt.scatter(2.90, 0, label = "AP1", color = 'orange')
            plt.scatter(1.45, 3.61, label = "AP2", color = 'yellow')
            plt.scatter(1.45, 7.22, label = "AP3", color = 'purple')  

            # #Garis Acuan Ruang 1
            # A = [0, 1.53]
            # B = [3.95, 1.53]
            # C = [3.95, 1.53]
            # D = [3.95, 4.10]

            #Garis Acuan Ruang 2
            A = [1.45, 0]
            B = [1.45, 7.22]
            C = [1.45, 0]
            D = [1.45, 7.22]
            
            EKf = [dataKF['x'].iloc[-1], dataKF['y'].iloc[-1]]
            E = [data['x'].iloc[-1], data['y'].iloc[-1]]

            # Calculate minimum distances
            min_dist_ABKf = minDistance(A, B, EKf)
            min_dist_CDKf = minDistance(C, D, EKf)
            if min_dist_ABKf < min_dist_CDKf:
                with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
                    with open("outputErrorTitikGaris(KF).csv", 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        info = {
                            "error": min_dist_ABKf,
                        }
                        csv_writer.writerow(info)
                print("Jarak Titik ke Garis Jalan (KF):", min_dist_ABKf)
            elif min_dist_ABKf > min_dist_CDKf:
                with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
                    with open("outputErrorTitikGaris(KF).csv", 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        info = {
                            "error": min_dist_CDKf,
                        }
                        csv_writer.writerow(info)
                print("Jarak Titik ke Garis Jalan (KF):", min_dist_CDKf)
            elif min_dist_ABKf == min_dist_CDKf:
                with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
                    with open("outputErrorTitikGaris(KF).csv", 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        info = {
                            "error": min_dist_ABKf,
                        }
                        csv_writer.writerow(info)
                print("Jarak Titik ke Garis Jalan (KF):", min_dist_ABKf)
            
            # Calculate minimum distances
            min_dist_AB = minDistance(A, B, E)
            min_dist_CD = minDistance(C, D, E)
            if min_dist_AB < min_dist_CD:
                with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
                    with open("outputErrorTitikGaris.csv", 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        info = {
                            "error": min_dist_AB,
                        }
                        csv_writer.writerow(info)
                print("Jarak Titik ke Garis Jalan :", min_dist_AB)
            elif min_dist_AB > min_dist_CD:
                with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
                    with open("outputErrorTitikGaris.csv", 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        info = {
                            "error": min_dist_CD,
                        }
                        csv_writer.writerow(info)
                print("Jarak Titik ke Garis Jalan :", min_dist_CD)
            elif min_dist_AB == min_dist_CD:
                with lock:  # Menggunakan lock untuk mengamankan akses ke file CSV
                    with open("outputErrorTitikGaris.csv", 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        info = {
                            "error": min_dist_AB,
                        }
                        csv_writer.writerow(info)
                print("Jarak Titik ke Garis Jalan :", min_dist_AB)

            plt.plot([A[0], B[0]], [A[1], B[1]], marker='o', label='Line Segment AB',color='green')
            plt.plot([C[0], D[0]], [C[1], D[1]], marker='o', label='Line Segment CD',color='green')

            plt.scatter(xKF, yKF, label='Prediksi Histori Kalman', color='blue')  # Menggunakan plt.scatter() untuk memplot titik-titik
            plt.scatter(x, y, label='Prediksi Tanpa Kalman', color='red')  # Menggunakan plt.scatter() untuk memplot titik-titik
            plt.scatter(dataKF['x'].iloc[-1], dataKF['y'].iloc[-1], label='Prediksi Kalman Sekarang', color='black')  # Menggunakan plt.scatter() untuk memplot titik-titik  

            plt.legend(loc='upper left')
            plt.tight_layout()
    except Exception as e:
        pass

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
    
    fieldnames = ["error"]
    outputErrorTitikGarisKf = f"outputErrorTitikGaris(KF).csv"
    with open(outputErrorTitikGarisKf, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
    
    outputErrorTitikGaris = f"outputErrorTitikGaris.csv"
    with open(outputErrorTitikGaris, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    try:
        plt.tight_layout()
        plt.show()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Closing the plot...")
        plt.close()  # Menutup plot saat menerima sinyal KeyboardInterrupt