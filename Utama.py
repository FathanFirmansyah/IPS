import os
import multiprocessing
import signal

def run_script(script_name):
    try:
        os.system(f"python {script_name}")
    except KeyboardInterrupt:
        pass  # Tangani KeyboardInterrupt di sini

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_IGN)  # Menangani sinyal KeyboardInterrupt untuk proses anak
    
    # Membuat proses untuk tes2.py
    p1 = multiprocessing.Process(target=run_script, args=("Wifi_RssiV6.py",))
    p1.start()
    print("Started tes2.py")

    # Membuat proses untuk tes3.py
    p2 = multiprocessing.Process(target=run_script, args=("Animate.py",))
    p2.start()
    print("Started tes3.py")

    # Menunggu kedua proses selesai
    p1.join()
    p2.join()
