import numpy as np

reference_rssi_dict = {
    "RuijieAP1": -31.24,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": -28.80,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": -32.70,   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
    "UIIConnect": -31.24,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "eduroam": -28.80,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
}

n_dict = {
    "RuijieAP1": 1.75,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "RuijieAP2": 1.75,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
    "RuijieAP3": 1.6,   # RSSI pada jarak referensi untuk SSID RuijieAP3 (dalam dBm)
    "UIIConnect": -31.24,  # RSSI pada jarak referensi untuk SSID RuijieAP1 (dalam dBm)
    "eduroam": -28.80,  # RSSI pada jarak referensi untuk SSID RuijieAP2 (dalam dBm)
}

ssid = "RuijieAP2"
ssidN = "RuijieAP2"
RSSI = -31

A = reference_rssi_dict[ssid]
n = n_dict[ssidN]
d = 10 ** ((A - RSSI) / (10 * n))
print (d)