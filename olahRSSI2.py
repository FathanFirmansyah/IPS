from filterpy.kalman import KalmanFilter
import numpy as np
import pandas as pd

# Path to the CSV file
input_csv_path = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\tes.csv'
output_csv_path = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\outputKF.csv'

# Define the dictionaries for path loss exponent and reference RSSI
n_dict = {
    "RuijieAP1": 3.34,
    "RuijieAP2": 2.3,
    "RuijieAP3": 2.99,
}

reference_rssi_dict = {
    "RuijieAP1": -23,
    "RuijieAP2": -23,
    "RuijieAP3": -21,
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

def calculate_distanceKalmanAP1(rssi, ssid, kfAP1, data_count):
    """
    Calculate the distance based on RSSI, reference RSSI (A), and path loss exponent (n).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        ssid (str): SSID of the access point.
        kf (KalmanFilter): Kalman filter instance for the access point.
        data_count (int): Index of the current data point.
    
    Returns:
        float: Distance between transmitter and receiver.
    """
    reference_rssi = reference_rssi_dict[ssid]
    n = n_dict[ssid]
    if data_count == 0:
        kfAP1.x = np.array([reference_rssi])
    kfAP1.predict()
    kfAP1.update(np.array([rssi]))

    estimated_rssi = kfAP1.x[0]
    distanceKalman = 10 ** ((reference_rssi - estimated_rssi) / (10 * n))
    return distanceKalman

def calculate_distanceKalmanAP2(rssi, ssid, kfAP2, data_count):
    """
    Calculate the distance based on RSSI, reference RSSI (A), and path loss exponent (n).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        ssid (str): SSID of the access point.
        kf (KalmanFilter): Kalman filter instance for the access point.
        data_count (int): Index of the current data point.
    
    Returns:
        float: Distance between transmitter and receiver.
    """
    reference_rssi = reference_rssi_dict[ssid]
    n = n_dict[ssid]
    if data_count == 0:
        kfAP2.x = np.array([reference_rssi])
    kfAP2.predict()
    kfAP2.update(np.array([rssi]))

    estimated_rssi = kfAP2.x[0]
    distanceKalman = 10 ** ((reference_rssi - estimated_rssi) / (10 * n))
    return distanceKalman

def calculate_distanceKalmanAP3(rssi, ssid, kfAP3, data_count):
    """
    Calculate the distance based on RSSI, reference RSSI (A), and path loss exponent (n).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        ssid (str): SSID of the access point.
        kf (KalmanFilter): Kalman filter instance for the access point.
        data_count (int): Index of the current data point.
    
    Returns:
        float: Distance between transmitter and receiver.
    """
    reference_rssi = reference_rssi_dict[ssid]
    n = n_dict[ssid]
    if data_count == 0:
        kfAP3.x = np.array([reference_rssi])
    kfAP3.predict()
    kfAP3.update(np.array([rssi]))

    estimated_rssi = kfAP3.x[0]
    distanceKalman = 10 ** ((reference_rssi - estimated_rssi) / (10 * n))
    return distanceKalman

# Read the CSV file
df = pd.read_csv(input_csv_path)

# Initialize an empty DataFrame to store distances
distance_data = {
    "RuijieAP1": [],
    "RuijieAP2": [],
    "RuijieAP3": []
}

data_count = 0
# Process each row in the CSV
for index, row in df.iterrows():
    distance_data["RuijieAP1"].append(calculate_distanceKalmanAP1(row['AP1'], "RuijieAP1", kfAP1, data_count))
    distance_data["RuijieAP2"].append(calculate_distanceKalmanAP2(row['AP2'], "RuijieAP2", kfAP2, data_count))
    distance_data["RuijieAP3"].append(calculate_distanceKalmanAP3(row['AP3'], "RuijieAP3", kfAP3, data_count))
    data_count +=1

# Create a new DataFrame with the calculated distances
distance_df = pd.DataFrame(distance_data)

# Write the new DataFrame to a CSV file
distance_df.to_csv(output_csv_path, index=False)

print(f"Distances have been calculated and saved to {output_csv_path}")
