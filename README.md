# Cypher-keylogger-v1: Educational Security PoC

## ⚠️ DISCLAMER
**This project is for educational and ethical security research purposes only.** Unauthorized use of this software against systems you do not have explicit permission to test is illegal and unethical. The author (demon-code-CypheR) is not responsible for any misuse or damage caused by this program.

## Overview
Cypher-keylogger-v1 is a Python-based tool designed to demonstrate how keyboard logging and administrative persistence function in a Windows environment. This project highlights:
* **Asymmetric-like Encryption:** Uses `cryptography.fernet` to encrypt logs locally.
* **Persistence:** Demonstrates Windows Registry manipulation to run on startup.
* **Stealth:** Uses `ctypes` to hide the console window from the user.
* **Environment Awareness:** Detects if it is running inside a Virtual Machine (VM).
* **Remote Kill-Switch:** Periodically checks a remote URL to stop execution if triggered.

## Technical Features
* **Language:** Python 3.14.
* **Libraries:** `pynput`, `cryptography`, `wmi`, `pywin32`.
* **Log Location:** Encrypted logs are stored in `%APPDATA%\WindowsUpdater.log`.

## Usage (For Research)
1. Install dependencies: `pip install pynput cryptography wmi pywin32 requests`
2. Run `generate_key.py` to create your local `encryption.key`.
3. Execute `keylogger_logic.py` to start the listener.
4. To stop: Press `ESC` or trigger the remote kill-switch.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
