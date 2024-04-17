import math

def calculate_path_loss_exponent(RSSI, A, d):
    """
    Calculate the path loss exponent (n) based on RSSI, reference RSSI (A), and distance (d).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        A (float): Reference RSSI at 1 meter.
        d (float): Distance between transmitter and receiver.
    
    Returns:
        float: Path loss exponent (n).
    """
    n = -(RSSI - A) / (10 * math.log10(d))
    return n

def calculate_RSSI(n, A, d):
    """
    Calculate the RSSI based on path loss exponent (n), reference RSSI (A), and distance (d).
    
    Parameters:
        n (float): Path loss exponent.
        A (float): Reference RSSI at 1 meter.
        d (float): Distance between transmitter and receiver.
    
    Returns:
        float: Received Signal Strength Indication (RSSI).
    """
    RSSI = -n * 10 * math.log10(d) + A
    return RSSI

def calculate_distance(RSSI, A, n):
    """
    Calculate the distance based on RSSI, reference RSSI (A), and path loss exponent (n).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        A (float): Reference RSSI at 1 meter.
        n (float): Path loss exponent.
    
    Returns:
        float: Distance between transmitter and receiver.
    """
    d = 10 ** ((A - RSSI) / (10 * n))
    return d

# Example usage:
RSSI_measurement = -70  # Contoh nilai RSSI yang diukur
A_reference_RSSI = -50  # Contoh nilai RSSI pada jarak referensi (biasanya diukur pada 1 meter)
distance = 10  # Contoh jarak antara transmitter dan receiver dalam meter

# Hitung path loss exponent (n) berdasarkan nilai RSSI yang diukur, RSSI pada jarak referensi, dan jarak
n = calculate_path_loss_exponent(RSSI_measurement, A_reference_RSSI, distance)
print("Path loss exponent (n):", n)

# Hitung RSSI berdasarkan path loss exponent (n), RSSI pada jarak referensi, dan jarak
estimated_RSSI = calculate_RSSI(n, A_reference_RSSI, distance)
print("Estimated RSSI:", estimated_RSSI)

path_loss_exponent = 2.0  # Contoh nilai path loss exponent

# Hitung jarak berdasarkan nilai RSSI yang diukur, RSSI pada jarak referensi, dan path loss exponent
distance = calculate_distance(RSSI_measurement, A_reference_RSSI, path_loss_exponent)
print("Estimated distance:", distance, "meters")
