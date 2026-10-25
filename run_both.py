#!/usr/bin/env python
"""
Launcher to run both ZIYO Storefront (Port 8000) and Management Portal (Port 8001) simultaneously.
"""
import subprocess
import sys
import time

def main():
    python_exe = sys.executable

    print("=" * 70)
    print("  LAUNCHING ZIYO DUAL-PORTAL ARCHITECTURE")
    print("  1. Customer Storefront   : http://127.0.0.1:8000/")
    print("  2. Management Portal     : http://127.0.0.1:8001/")
    print("=" * 70)

    # Spawn storefront
    p_storefront = subprocess.Popen(
        [python_exe, "run_storefront.py", "127.0.0.1:8000"],
    )

    time.sleep(1)

    # Spawn management portal
    p_management = subprocess.Popen(
        [python_exe, "run_management.py", "127.0.0.1:8001"],
    )

    try:
        p_storefront.wait()
        p_management.wait()
    except KeyboardInterrupt:
        print("\nStopping both servers gracefully...")
        p_storefront.terminate()
        p_management.terminate()
        p_storefront.wait()
        p_management.wait()
        print("Both servers stopped.")

if __name__ == "__main__":
    main()
