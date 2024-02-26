import numpy as np

def trilaterasi(P1, P2, P3, DistA, DistB, DistC):
    """
    Trilaterasi untuk menemukan koordinat titik yang tidak diketahui berdasarkan tiga titik yang diketahui
    dan jaraknya dari titik tersebut.

    Args:
    - P1, P2, P3: Titik-titik yang diketahui sebagai numpy array, misalnya P1 = np.array([x1, y1, z1]).
    - DistA, DistB, DistC: Jarak dari titik-titik tersebut ke titik yang tidak diketahui.

    Returns:
    - triPt: Koordinat titik yang tidak diketahui sebagai numpy array.
    """

    # Hitung vektor arah dari P1 ke P2 (ex)
    ex = (P2 - P1) / np.linalg.norm(P2 - P1)

    # Hitung vektor dari P1 ke P3 (p3p1)
    p3p1 = P3 - P1

    # Hitung proyeksi dari vektor p3p1 ke vektor ex (ival)
    ival = np.dot(ex, p3p1)

    # Hitung vektor arah dari P3 ke titik yang tidak diketahui (ey)
    ey = (P3 - P1 - ival * ex) / np.linalg.norm(P3 - P1 - ival * ex)

    # Hitung vektor tegak lurus terhadap ex dan ey (ez)
    if len(P1) == 2:
        ez = np.array([0, 0])
    else:
        ez = np.cross(ex, ey)

    # Hitung jarak antara P1 dan P2 (d)
    d = np.linalg.norm(P2 - P1)

    # Hitung proyeksi dari vektor p3p1 ke vektor ey (jval)
    jval = np.dot(ey, p3p1)

    # Hitung koordinat x titik yang tidak diketahui (xval)
    xval = (DistA**2 - DistB**2 + d**2) / (2 * d)

    # Hitung koordinat y titik yang tidak diketahui (yval)
    yval = ((DistA**2 - DistC**2 + ival**2 + jval**2) / (2 * jval)) - (ival / jval) * xval

    # Hitung koordinat z titik yang tidak diketahui (zval)
    zval = np.sqrt(DistA**2 - xval**2 - yval**2) if len(P1) == 3 else 0

    # Hitung koordinat titik yang tidak diketahui (triPt)
    triPt = P1 + xval * ex + yval * ey + zval * ez

    return triPt

# Contoh penggunaan:
P1 = np.array([0, 0])
P2 = np.array([0, -6.3])
P3 = np.array([5, -6])
DistA = 1.7
DistB = 5
DistC = 7.3

titik_tidak_diketahui = trilaterasi(P1, P2, P3, DistA, DistB, DistC)
print("Koordinat titik yang tidak diketahui:", titik_tidak_diketahui)
