import numpy as np

# Initialize the filter with an initial estimate of the position and the associated uncertainty (covariance)
x_estimated = 0
P_estimated = 1

# Define the velocity and the process noise
velocity = 1
process_noise = 0.1

# Define the measurement noise
measurement_noise = 0.1

for i in range(10):
    # Generate a measurement with some random noise
    measurement = i + np.random.normal(0, measurement_noise)

    # Prediction step
    x_predicted = x_estimated + velocity
    P_predicted = P_estimated + process_noise

    # Correction step
    Kf = P_predicted / (P_predicted + measurement_noise)
    x_estimated = x_predicted + Kf * (measurement - x_predicted)
    P_estimated = (1 - Kf) * P_predicted

    # Print the estimated position
    print("Estimated position: ", x_estimated)