import os
import subprocess

def is_ip_alive(ip_address):
    try:
        ping_command = f"ping -n 1 {ip_address}" if os.name == 'nt' else f"ping -c 1 {ip_address}"
        response = subprocess.run(ping_command, shell=True, capture_output=True, text=True)
        return response.returncode == 0
    except Exception as e:
        print(f"Error checking IP {ip_address}: {e}")
        return False