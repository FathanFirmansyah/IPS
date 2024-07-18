# Olah rssi tanpa kalman menjadi jarak
import pandas as pd

# Path to the CSV file
input_csv_path = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\tes.csv'
output_csv_path = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\outputJarak.csv'

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

def calculate_distance(RSSI, ssid):
    """
    Calculate the distance based on RSSI, reference RSSI (A), and path loss exponent (n).
    
    Parameters:
        RSSI (float): Received Signal Strength Indication.
        ssid (str): SSID of the access point.
    
    Returns:
        float: Distance between transmitter and receiver.
    """
    A = reference_rssi_dict[ssid]
    n = n_dict[ssid]
    d = 10 ** ((A - RSSI) / (10 * n))
    return d

# Read the CSV file
df = pd.read_csv(input_csv_path)

# Calculate distances and create a new DataFrame
distance_data = {
    "RuijieAP1": [],
    "RuijieAP2": [],
    "RuijieAP3": []
}

for index, row in df.iterrows():
    distance_data["RuijieAP1"].append(calculate_distance(row['AP1'], "RuijieAP1"))
    distance_data["RuijieAP2"].append(calculate_distance(row['AP2'], "RuijieAP2"))
    distance_data["RuijieAP3"].append(calculate_distance(row['AP3'], "RuijieAP3"))

# Create a new DataFrame with the calculated distances
distance_df = pd.DataFrame(distance_data)

# Write the new DataFrame to a CSV file
distance_df.to_csv(output_csv_path, index=False)

print(f"Distances have been calculated and saved to {output_csv_path}")
