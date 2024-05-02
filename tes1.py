import numpy as np
import matplotlib.pyplot as plt

beacon_positions = {
    "RuijieAP1": np.array([0, 0]),
    "RuijieAP2": np.array([5.76, 0]),
    "RuijieAP3": np.array([5.76, 5.16])
}

def trilateration(ssid1, rAP1, ssid2, rAP2, ssid3, rAP3):
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
    return x, y

AP1 = [2.503151265,
3.035429268,
3.82797084,
5.158552668,
5.176833841,
6.194033005,
4.246518218,
4.890397913,
5.195539866
]
AP2 = [2.791697504,
5.469422318,
5.348197156,
3.881148747,
4.742533802,
3.433787299,
3.084585015,
2.377065906,
4.864226739
]
AP3 = [3.0348116,
5.271856155,
7.653219803,
5.97480443,
8.621998943,
3.568919631,
5.615075944,
6.711291271,
4.832243664
]

AP1KF = [1.78902,
2.63968,
3.41578,
4.3683,
4.31298,
5.07982,
4.81988,
4.33642,
5.01222
]
AP2KF = [1.6072,
3.23012,
2.82254,
3.12594,
3.25854,
3.14672,
3.08556,
2.58358,
3.21022
]
AP3KF = [1.81876,
3.81976,
6.11528,
6.16106,
7.77776,
4.28672,
4.72984,
6.09708,
5.29614
]

fig, ax = plt.subplots()
all_x = []
all_y = []
for i in range(len(AP1)):
    x1, y1 = trilateration("RuijieAP1", AP1[i], "RuijieAP2", AP2[i], "RuijieAP3", AP3[i])
    all_x.append(x1)
    all_y.append(y1)
    ax.scatter(x1, y1, color='red', label='Prediksi Tanpa Kalman' if i == 0 else None)
    x2, y2 = trilateration("RuijieAP1", AP1KF[i], "RuijieAP2", AP2KF[i], "RuijieAP3", AP3KF[i])
    all_x.append(x2)
    all_y.append(y2)
    ax.scatter(x2, y2, color='blue', label='Prediksi Kalman Filter' if i == 0 else None)
    print(x2)   

# Definisikan koordinat titik-titik persegi panjang
x = [0, 5.76, 5.76, 2.15, 2.15, 0, 0]
y = [0, 0, 5.16, 5.16, 3.06, 3.06, 0]

# Gambar persegi panjang
ax.plot(x, y)

# Atur batas sumbu x dan y berdasarkan nilai maksimum dari semua hasil x dan y
max_x = max(all_x)
min_x = min(all_x)
max_y = max(all_y)
min_y = min(all_y)

max_x += 10
min_x -= 10
max_y += 10
min_y -= 10

ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

# Tambahkan titik pada koordinat asli (0, 1.53)
# ax.scatter(0, 1.53, color='green', label='Asli')

# Tampilkan legenda
ax.legend()

# Tampilkan gambar
plt.show()
