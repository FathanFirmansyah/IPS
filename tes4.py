#Fungsi untuk menghitung jarak antara 1 titik ke titik lainnya dalam 2 dimensi menggunakan rumus eucladian
import math

# Koordinat titik pertama
x1, y1 = 0, 1.53

# Koordinat titik kedua
x2, y2 = -12.311927344746328, 18.763626425136295

# Menghitung jarak menggunakan rumus jarak Euclidean
jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
jarak_dua_desimal = round(jarak, 2)
print(jarak_dua_desimal)
