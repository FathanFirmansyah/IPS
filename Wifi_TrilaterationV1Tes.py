import math

def trilaterate(beacons, distances):
    """
    Trilateration untuk menentukan posisi pengguna berdasarkan jarak yang diterima dari beberapa beacon.
    
    Args:
        beacons (list): List koordinat beacon dalam format (x, y).
        distances (list): List jarak antara pengguna dan masing-masing beacon.
    
    Returns:
        tuple: Koordinat perkiraan posisi pengguna dalam format (x, y).
    """
    x1, y1 = beacons[0]  # Koordinat beacon A
    x2, y2 = beacons[1]  # Koordinat beacon B
    x3, y3 = beacons[2]  # Koordinat beacon C
    d1, d2, d3 = distances  # Jarak dari pengguna ke masing-masing beacon
    
    # Hitung posisi perkiraan pengguna
    x = (d1**2 - d2**2 + x2**2 - x1**2 + y2**2 - y1**2) / (2 * (x2 - x1))
    y = (d1**2 - d3**2 + x3**2 - x1**2 + y3**2 - y1**2) / (2 * (y3 - y1))
    
    return x, y

# Definisikan koordinat beacon dan jarak-jaraknya
beacons = [(2, 0), (5, 1), (1, 5)]
distances = [4, 4, 3]

# Hitung posisi perkiraan pengguna
user_position = trilaterate(beacons, distances)
print("Posisi pengguna perkiraan:", user_position)


