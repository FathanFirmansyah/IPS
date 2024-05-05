#Fungsi untuk menunjukkan garis putus-putus dari titik ke garis jalan
import matplotlib.pyplot as plt
from math import sqrt

# Function to return the minimum distance 
# between a line segment and a point
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

# Function to project point E onto the line segment AB and CD
def project_point(A, B, E):
    AB = [B[0] - A[0], B[1] - A[1]]
    AE = [E[0] - A[0], E[1] - A[1]]

    ab_magnitude = sqrt(AB[0]**2 + AB[1]**2)
    ab_unit_vector = [AB[0] / ab_magnitude, AB[1] / ab_magnitude]

    # Project E onto AB
    dot_product = AE[0] * ab_unit_vector[0] + AE[1] * ab_unit_vector[1]
    projected_point = [A[0] + dot_product * ab_unit_vector[0], A[1] + dot_product * ab_unit_vector[1]]

    # Ensure the projected point lies within the line segment AB
    if dot_product < 0:
        projected_point = A
    elif dot_product > ab_magnitude:
        projected_point = B

    return projected_point

# Function to plot line segments and point E
def plot_segments_and_point(A, B, C, D, E, min_dist_AB, min_dist_CD):
    plt.plot([A[0], B[0]], [A[1], B[1]], marker='o', label='Line Segment AB')
    plt.plot([C[0], D[0]], [C[1], D[1]], marker='o', label='Line Segment CD')
    plt.plot(E[0], E[1], marker='o', label='Point E')

    # Project point E onto AB and CD
    projected_point_AB = project_point(A, B, E)
    projected_point_CD = project_point(C, D, E)

    # Plot perpendicular for minimum distance to AB
    plt.plot([E[0], projected_point_AB[0]], [E[1], projected_point_AB[1]],
             linestyle='--', color='r', label='Perpendicular to AB')

    # Plot perpendicular for minimum distance to CD
    plt.plot([E[0], projected_point_CD[0]], [E[1], projected_point_CD[1]],
             linestyle='--', color='g', label='Perpendicular to CD')

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Minimum Distance Visualization')
    plt.legend()
    plt.grid(True)
    plt.show()

# Driver code 
if __name__ == "__main__" :
    A = [0, 1.53]
    B = [3.94, 1.53]
    C = [3.94, 1.53]
    D = [3.94, 4.09]
    E = [1, 7.5]

    # Calculate minimum distances
    min_dist_AB = minDistance(A, B, E)
    min_dist_CD = minDistance(C, D, E)
    print("Minimum distance to AB:", min_dist_AB)
    print("Minimum distance to CD:", min_dist_CD)

    plot_segments_and_point(A, B, C, D, E, min_dist_AB, min_dist_CD)
