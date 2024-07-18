import pandas as pd
import numpy as np
from math import sqrt

# Path to the CSV file
input_csv_path = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\outputTrilaterasiKF.csv'
output_csv_path = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\outputErrorTitikGaris(KF).csv'

# Read the CSV file
df = pd.read_csv(input_csv_path)

# Define points A and B
A = [1.45, 0]
B = [1.45, 7.22]

# Function to calculate the minimum distance from point E to line segment AB
def minDistance(A, B, E):
    AB = [B[0] - A[0], B[1] - A[1]]
    BE = [E[0] - B[0], E[1] - B[1]]
    AE = [E[0] - A[0], E[1] - A[1]]

    AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1]

    reqAns = 0

    if AB_BE > 0:
        reqAns = sqrt(BE[0] * BE[0] + BE[1] * BE[1])
    elif AB_AE < 0:
        reqAns = sqrt(AE[0] * AE[0] + AE[1] * AE[1])
    else:
        reqAns = abs(AB[0] * AE[1] - AB[1] * AE[0]) / sqrt(AB[0] * AB[0] + AB[1] * AB[1])

    return reqAns

# Extract x and y coordinates
x_coords = df['x'].values
y_coords = df['y'].values

# Calculate distances for each point in the CSV file
distances = []
for x, y in zip(x_coords, y_coords):
    E = [x, y]
    distance = minDistance(A, B, E)
    distances.append(distance)

# Create a new DataFrame with the distances
distance_df = pd.DataFrame(distances, columns=['error'])

# Display the DataFrame
print(distance_df)

# Save the results to a new CSV file

distance_df.to_csv(output_csv_path, index=False, float_format='%.8f')

print(f"Distances have been saved to {output_csv_path}")
