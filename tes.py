import numpy as np

beacon_positions = {
    "RuijieAP1": np.array([0, 0]),
    "RuijieAP2": np.array([0, -6.3]),
    "RuijieAP3": np.array([5.9, -6.3])
}

print(beacon_positions["RuijieAP3"][1])