import numpy as np
import pandas as pd

def trilateration(ssid1, rAP1, ssid2, rAP2, ssid3, rAP3):
    """
    Trilateration untuk menentukan posisi pengguna berdasarkan sinyal yang diterima dari beberapa beacon.
    
    Args:
        ssid1, ssid2, ssid3 (str): SSID dari beacon.
        rAP1, rAP2, rAP3 (float): Jarak dari masing-masing beacon ke pengguna.
    
    Returns:
        tuple: Koordinat perkiraan posisi pengguna dalam format (x, y).
    """
    xAP1 = beacon_positions[ssid1][0]
    yAP1 = beacon_positions[ssid1][1]
    xAP2 = beacon_positions[ssid2][0]
    yAP2 = beacon_positions[ssid2][1]
    xAP3 = beacon_positions[ssid3][0]
    yAP3 = beacon_positions[ssid3][1]

    A = 2 * xAP2 - 2 * xAP1
    B = 2 * yAP2 - 2 * yAP1
    C = rAP1**2 - rAP2**2 - xAP1**2 + xAP2**2 - yAP1**2 + yAP2**2
    D = 2 * xAP3 - 2 * xAP2
    E = 2 * yAP3 - 2 * yAP2
    F = rAP2**2 - rAP3**2 - xAP2**2 + xAP3**2 - yAP2**2 + yAP3**2
    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)
    return x, y

# Ruang 1, Posisi 1
beacon_positions = {
    "RuijieAP1": np.array([2.90, 0]),
    "RuijieAP2": np.array([0, 3.61]),
    "RuijieAP3": np.array([2.90, 7.22])
}

# Baca nilai dari file CSV
csv_file = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\1\Data Benar\outputJarak.csv'  # Gunakan r prefix untuk string mentah
df = pd.read_csv(csv_file)

# Asumsi kolom CSV berisi nilai-nilai meanAP1, meanAP2, meanAP3 dalam urutan yang benar
meanAP1 = df['RuijieAP1'].iloc[0]
meanAP2 = df['RuijieAP2'].iloc[0]
meanAP3 = df['RuijieAP3'].iloc[0]

print(meanAP1, meanAP2, meanAP3)

x, y = trilateration("RuijieAP1", meanAP1, "RuijieAP2", meanAP2, "RuijieAP3", meanAP3)
print(x, y)
