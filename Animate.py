import signal
import sys
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

plt.style.use('fivethirtyeight')

def signal_handler(sig, frame):
    print("\n----------------EXIT----------------")
    sys.exit(0)

def animate(i):
    try:
        dataKF = pd.read_csv('outputTrilaterasiKF.csv')
        data = pd.read_csv('outputTrilaterasi.csv')
        if not dataKF.empty and not data.empty:
            xKF = dataKF['x']
            yKF = dataKF['y']

            x = data['x']
            y = data['y']

            plt.cla()

            # Gambar persegi panjang
            plt.plot([0, 5.76, 5.76, 2.15, 2.15, 0, 0], [0, 0, 5.16, 5.16, 3.06, 3.06, 0])

            plt.scatter(xKF, yKF, label='Prediksi Kalman', color='blue')  # Menggunakan plt.scatter() untuk memplot titik-titik
            plt.scatter(x, y, label='Prediksi Tanpa Kalman', color='red')  # Menggunakan plt.scatter() untuk memplot titik-titik

            plt.legend(loc='upper left')
            plt.tight_layout()
    except Exception as e:
        pass

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
    
    try:
        plt.tight_layout()
        plt.show()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Closing the plot...")
        plt.close()  # Menutup plot saat menerima sinyal KeyboardInterrupt
