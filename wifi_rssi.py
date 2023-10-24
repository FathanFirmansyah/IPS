import time
import pywifi

# Parameter-parameter untuk Model Path Loss
reference_rssi = -32  # RSSI pada jarak referensi 1 Meter (dalam dBm)
n = 2.0  # Path Loss Exponent (biasanya berkisar antara 2.0 hingga 4.0)

def calculate_distance(rssi):
    ratio = (reference_rssi-rssi) / (10 *n)
    distance = 10 ** ratio
    return distance

def scan_wifi_rssi(ssid, output_file):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Menggunakan antarmuka pertama (biasanya wlan0)

    try:
        while True:
            iface.scan()
            time.sleep(2)
            scan_results = iface.scan_results()

            for result in scan_results:
                if ssid in result.ssid:
                    rssi = result.signal
                    distance = calculate_distance(rssi)
                    with open(output_file, "a") as file:
                        file.write(f"{ssid}: RSSI={rssi} dBm, Jarak={distance:.2f} meter\n")
                    return rssi

            print(f"Tidak dapat menemukan {ssid}")
            time.sleep(2)  # Interval cek setiap 2 detik
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    target_ssid = input("Masukkan nama SSID jaringan WiFi yang ingin Anda monitor: ")
    output_file = "tes.txt"  # Ganti dengan nama file yang Anda inginkan

    try:
        while True:
            rssi = scan_wifi_rssi(target_ssid, output_file)

            if rssi is not None:
                print(f"{target_ssid}: RSSI={rssi} dBm")
            else:
                print(f"Tidak dapat menemukan {target_ssid}")

    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna (Ctrl+C)")
