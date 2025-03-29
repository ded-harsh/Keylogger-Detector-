import psutil
import os
import ctypes
import time

LOG_FILE = "keylogger_detector.log"

# Suspicious keywords commonly found in keyloggers
KNOWN_KEYLOGGERS = ["keylogger", "hook", "keyboard", "spy", "stealth", "sniffer", "logger", "capture"]

def log_suspicious_activity(message):
    """Log and print suspicious activities."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)

def check_suspicious_processes():
    """Check for suspicious processes and attempt to terminate them."""
    for process in psutil.process_iter(['pid', 'name']):
        process_name = process.info['name'].lower()
        for keyword in KNOWN_KEYLOGGERS:
            if keyword in process_name:
                pid = process.info['pid']
                log_suspicious_activity(f"[!] Suspicious process detected: {process_name} (PID: {pid})")
                terminate_process(pid)

def terminate_process(pid):
    """Attempt to terminate a suspicious process."""
    try:
        process = psutil.Process(pid)
        process.terminate()
        log_suspicious_activity(f"[✔] Terminated suspicious process: {pid}")
    except Exception as e:
        log_suspicious_activity(f"[X] Failed to terminate process {pid}: {str(e)}")

def check_keyboard_hooks():
    """Detect possible keyboard hooks."""
    user32 = ctypes.windll.user32
    hook_check = user32.GetAsyncKeyState(0x02)  # Checking right-click hook
    if hook_check != 0:
        log_suspicious_activity("[!] Potential keyboard hook detected!")

def monitor_system():
    """Continuously monitor for keyloggers."""
    print("🔍 Real-time Keylogger Monitoring Started...")
    while True:
        check_suspicious_processes()
        check_keyboard_hooks()
        time.sleep(10)  # Adjust the scan interval as needed

if __name__ == "__main__":
    try:
        monitor_system()
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped by user.")
      
