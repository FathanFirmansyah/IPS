import pandas as pd
import re

# Define the file path
file_path = r'Data Penelitian/Data Final v4/Dinamis/Ruang 2/Ruang Isi/Posisi 1/5/Data benar/outputRSSI.csv'  # Using raw string to avoid invalid escape sequences
output_csv_path = r'Data Penelitian/Data Final v4/Dinamis/Ruang 2/Ruang Isi/Posisi 1/5/Data benar/tes.csv'

# Read the CSV file
df = pd.read_csv(file_path, header=None, names=['Data'])

# Function to extract AP name and numeric RSSI value
def extract_ap_rssi(row):
    match = re.match(r'RSSI (\w+) = (-?\d+) dBm', row)
    if match:
        ap_name, rssi_value = match.groups()
        return ap_name, int(rssi_value)
    return None, None

# Apply the function to the DataFrame
df[['AP', 'RSSI']] = df['Data'].apply(lambda x: pd.Series(extract_ap_rssi(x)))

# Drop the original Data column
df = df.drop(columns=['Data'])

# Split the data into separate DataFrames for each AP
df_ruijieap1 = df[df['AP'] == 'RuijieAP1'].drop(columns=['AP'])
df_ruijieap2 = df[df['AP'] == 'RuijieAP2'].drop(columns=['AP'])
df_ruijieap3 = df[df['AP'] == 'RuijieAP3'].drop(columns=['AP'])

# Merge the separate DataFrames into a single DataFrame
merged_df = pd.concat([df_ruijieap1.reset_index(drop=True), df_ruijieap2.reset_index(drop=True), df_ruijieap3.reset_index(drop=True)], axis=1)
merged_df.columns = ['AP1', 'AP2', 'AP3']

# Save to a CSV file
merged_df.to_csv(output_csv_path, index=False, header=True)

print(f"File has been saved to {output_csv_path}")
