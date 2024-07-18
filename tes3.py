#Hitung manual Trilaterasi menggunakan nilai output jarak
import numpy as np

# Ruang 2, Posisi 2
beacon_positions = {
    "RuijieAP1": [2.90, 0],
    "RuijieAP2": [1.45, 3.61],
    "RuijieAP3": [1.45, 7.22]
}

# AP1 = [
#     1.2026,
#     1.2730,
#     1.3929,
#     1.4064,
#     1.4894,
#     1.5065,
#     1.5177,
#     1.4862,
#     1.5045,
#     1.4779,
#     1.5782,
#     1.4853,
#     1.5430,
#     1.5412,
#     1.5801,
#     1.5251,
#     1.5695,
#     1.5186,
#     1.5254,
#     1.4532
#     ]
# AP2 = [
#     1.3847,
#     1.7130,
#     2.1677,
#     2.2625,
#     2.7683,
#     2.7272,
#     3.2167,
#     3.0917,
#     3.3868,
#     3.1038,
#     3.2978,
#     3.0512,
#     3.3583,
#     3.0870,
#     3.3835,
#     3.1019,
#     3.3940,
#     3.2000,
#     3.3630,
#     3.0898
#     ]
# AP3 = [
#     1.6197,
#     2.4021,
#     3.5267,
#     3.5335,
#     4.7777,
#     4.2034,
#     5.1237,
#     4.3951,
#     5.2735,
#     4.3812,
#     5.2629,
#     4.3756,
#     5.1462,
#     4.4072,
#     4.9515,
#     4.2995,
#     4.9799,
#     4.3152,
#     4.7806,
#     4.2036
#     ]

# meanAP1 = np.nanmean(AP1)
# meanAP2 = np.nanmean(AP2)
# meanAP3 = np.nanmean(AP3)

meanAP1 = 2.45031295898047
meanAP2 = 6.309573444801933
meanAP3 =2.771123846484588

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

print(meanAP1,meanAP2,meanAP3)

x,y = trilateration("RuijieAP1",meanAP1,"RuijieAP2",meanAP2,"RuijieAP3",meanAP3)
print (x,y)