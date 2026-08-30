# Port Scanner
A Port Scanner built with Python and PyQt5. Enter a target IP/hostname to get information on the ports that are open. 

<img width="494" height="625" alt="Screenshot 2026-08-30 at 1 24 42 AM" src="https://github.com/user-attachments/assets/612c898e-44c4-4919-8c99-c55b9c1bffa9" />

## Features
- Multithreaded scanning (up to 100 concurrent ports) using `ThreadPoolExecutor`
- Simple PyQt5 GUI: Enter a target IP/hostname and scan.
- Scans all ports (1-65535) and lists which are open in real time.
- Handles invalid/unresolvable hostnames.
## Tech Stack
- Python 3: Core language.
- **`socket`**: Low level TCP connections used to test whether each port is open.
- **`concurrent.futures.ThreadPoolExecutor`**: Runs up to 100 port-scan tasks simultaneously instead of sequentially.
- **`PyQt5`**: GUI framework.
- **`QThread`** and **`pyqtSignal`**: Run scans off the main thread so the interface stays responsive.
- **`datetime`**: Timestamps scan start/finish times.

## How it Evolved
This started as a simple sequential CLI scanner (one part checked at a time), then it went through two major upgrades:
1. **Multithreading**: Replaced the single-threaded loop with a `ThreadPoolExecutor` pool of 100 worker threads, so ports are checked simultaneously instead of one at a time. Significantly increased the scan time.
2. **GUI Integration**: Wrapped the scanning logic in a `QThread` subclass so it runs off the main UI thread. Results stream back to the interface live via Qt signals (`pyqtSignal`) as each open port is found.

## Setup
1. Clone the repository:
```
git clone https://github.com/nnoglo/port-scanner.git
cd port-scanner
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the scanner:
```
python port_scanner_gui.py
```

## Disclaimer
Only scan hosts you own or have explicit permission to scan.

### License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/nnoglo/port-scanner/blob/main/LICENSE) file for details.
