import numpy as np

# Define the points and distances
P1 = np.array([2, 0])
P2 = np.array([8, 0])
P3 = np.array([4, 10])

DistA = 6
DistB = 6
DistC = 6

# Calculate ex
ex = (P2 - P1) / np.linalg.norm(P2 - P1)

# Calculate p3p1
p3p1 = P3 - P1

# Calculate ival
ival = np.dot(ex, p3p1)

# Calculate ey
ey = (P3 - P1 - ival * ex) / np.linalg.norm(P3 - P1 - ival * ex)

# Calculate ez
if len(P1) == 2:
    ez = np.array([0, 0])
else:
    ez = np.cross(ex, ey)

# Calculate d
d = np.linalg.norm(P2 - P1)

# Calculate j
jval = np.dot(ey, p3p1)

# Calculate x
xval = (DistA**2 - DistB**2 + d**2) / (2 * d)

# Calculate y
yval = ((DistA**2 - DistC**2 + ival**2 + jval**2) / (2 * jval)) - (ival / jval) * xval

# Calculate z
zval = np.sqrt(DistA**2 - xval**2 - yval**2) if len(P1) == 3 else 0

# Calculate triPt
triPt = P1 + xval * ex + yval * ey + zval * ez

print("ex:", ex)
print("i:", ival)
print("ey:", ey)
print("d:", d)
print("j:", jval)
print("x:", xval)
print("y:", yval)
print("z:", zval)
print("final result:", triPt)
