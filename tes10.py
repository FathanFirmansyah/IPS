import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Path to the CSV file
input_csv_path = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\outputTrilaterasi.csv'
input_csv_pathKF = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\outputTrilaterasiKF.csv'

# Read the CSV file
df = pd.read_csv(input_csv_path)
dfKF = pd.read_csv(input_csv_pathKF)

# Extract x and y coordinates
x_coords = df['x']
y_coords = df['y']

x_coordsKF = dfKF['x']
y_coordsKF = dfKF['y']

# Create the plot
fig, ax = plt.subplots()

# Gambar Ruang 2
ax.plot([0, 2.90, 2.90, 0, 0], [0, 0, 7.22, 7.22, 0], label='Ruang 2')

# AP Ruang 2 Posisi 1
ax.scatter(2.90, 0, label="AP1", color='orange')
ax.scatter(0, 3.61, label="AP2", color='yellow')
ax.scatter(2.90, 7.22, label="AP3", color='purple')

# Garis Acuan Ruang 2
A = [1.45, 0]
B = [1.45, 7.22]
C = [1.45, 0]
D = [1.45, 7.22]

ax.plot([A[0], B[0]], [A[1], B[1]], 'g--', label='Garis Acuan Vertikal')
ax.plot([C[0], D[0]], [C[1], D[1]], 'g--')

# Adding labels and legend
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_title('Trilateration Results in Ruang 2')
ax.legend()

# Disable grid
ax.grid(False)

# Set limits for zoom out effect
ax.set_xlim(-2, 10)
ax.set_ylim(-10, 10)

# Initialize the scatter plot for trilateration results
sc_trilateration, = ax.plot([], [], 'ro', label='Trilateration Results')
sc_trilaterationKF, = ax.plot([], [], 'bo', label='Trilateration Results with KF')

def init():
    sc_trilateration.set_data([], [])
    sc_trilaterationKF.set_data([], [])
    return sc_trilateration, sc_trilaterationKF

def update(frame):
    sc_trilateration.set_data(x_coords[:frame+1], y_coords[:frame+1])
    sc_trilaterationKF.set_data(x_coordsKF[:frame+1], y_coordsKF[:frame+1])
    return sc_trilateration, sc_trilaterationKF

# Create animation
ani = FuncAnimation(fig, update, frames=len(x_coords), init_func=init, blit=True, repeat=False, interval=500)

# Show the plot
plt.show()
