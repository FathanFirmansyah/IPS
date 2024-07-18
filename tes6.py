# Kode untuk menganalisis nilai dinamis
import pandas as pd

def calculate_average_error(df, column_name='error'):
    if column_name in df.columns:
        # Mengambil nilai angka dari kolom "error"
        error_values = df[column_name].dropna().astype(float)
        # Menghitung rata-rata nilai error
        average_error = error_values.mean()
        # Membulatkan rata-rata nilai error hingga dua digit di belakang koma
        return round(average_error, 2)
    else:
        raise ValueError(f"Kolom '{column_name}' tidak ditemukan dalam file CSV.")

# Path file CSV pertama
file_path1 = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\outputErrorTitikGaris.csv'  # Ganti dengan path file CSV pertama Anda
# C:\Users\Fathan Firmansyah\Desktop\TES\Data Penelitian\Data Final v4\Dinamis\Ruang 1\Ruang Kosong\Posisi 1\Data Penelitian\4. Jalan\1
# C:\Users\Fathan Firmansyah\Desktop\TES\Data Penelitian\Data Final v4\Dinamis\Ruang 1\Ruang Isi\Posisi 1\1
# C:\Users\Fathan Firmansyah\Desktop\TES\Data Penelitian\Data Final v4\Dinamis\Ruang 1\Ruang Isi\Posisi 2\1
# C:\Users\Fathan Firmansyah\Desktop\TES\Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Kosong\Posisi 1\Data Pengujian\4. Jalan\1
# C:\Users\Fathan Firmansyah\Desktop\TES\Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\1\Data benar

# Path file CSV kedua
file_path2 = r'Data Penelitian\Data Final v4\Dinamis\Ruang 2\Ruang Isi\Posisi 1\5\Data benar\outputErrorTitikGaris(KF).csv'  # Ganti dengan path file CSV kedua Anda
# C:\Users\Fathan Firmansyah\Desktop\TES\Data Penelitian\Data Final v4\Dinamis\Ruang 1\Ruang Kosong\Posisi 1\Data Penelitian\4. Jalan\1

# Membaca file CSV pertama
df1 = pd.read_csv(file_path1)

# Membaca file CSV kedua
df2 = pd.read_csv(file_path2)


try:
    # Menghitung rata-rata nilai error dari file pertama
    average_error1 = calculate_average_error(df1)
    
    # Menghitung rata-rata nilai error dari file kedua
    average_error2 = calculate_average_error(df2)
    
    # Menghitung perubahan error dalam persen
    error_change_percent = ((average_error1 - average_error2) / average_error1) * 100
    error_change_percent = round(error_change_percent, 2)  # Membulatkan hingga dua digit di belakang koma
    
    print(f"Rata-rata nilai error -KF,+KF,Penurunan Error: {average_error1},{average_error2},{error_change_percent}")
    # print(f"Rata-rata nilai error +KF: {average_error2}")
    # print(f"Penurunan nilai error: {error_change_percent}%")
except ValueError as e:
    print(e)
