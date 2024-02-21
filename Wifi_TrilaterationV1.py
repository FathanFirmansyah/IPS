import numpy as np

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

# Contoh penggunaan
beacons = [(0, 0), (5, 0), (0, 5)]  # Koordinat beacon
distances = [3, 4, 5]  # Jarak dari pengguna ke masing-masing beacon

# Hitung posisi perkiraan pengguna
user_position = trilaterate(beacons, distances)

print("Posisi pengguna perkiraan:", user_position)
