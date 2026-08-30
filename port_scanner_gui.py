import socket # Importing the socket library to let different programs talk to each other over a network/the Internet
import sys # Gives us access to CLI (command line) arguments.
from datetime import datetime # Importing the datetime module to get the exact time when we scan the port.
from concurrent.futures import ThreadPoolExecutor # Importing this for multithreading
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, # Importing this for our GUI
                             QPushButton, QVBoxLayout, QListWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal # Importing this for our GUI

class ScannerThread(QThread): # This thread will send back three kinds of messages
    port_found = pyqtSignal(int) # A message that sends back a port number
    finished_scan = pyqtSignal() # Sends back a message once the scan is finished
    error_occurred = pyqtSignal(str) # Sends back an error message

    def __init__(self, target_input):
        super().__init__()
        self.target_input = target_input

    def scan_port(self, target, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a new network socket configured for TCP/IP communication.
        socket.setdefaulttimeout(1) # Sets a global timeout of 1 second for newly created socket objects.
        result = s.connect_ex((target, port)) # Returns an error (0 if the operation succeeded.)
        if result == 0: # If our error indicator is zero, then we will print which ports are open. 
            self.port_found.emit(port)
        s.close() # Closes the operation

    def run(self): # Runs when we do start()
        try:
          target_ip = socket.gethostbyname(self.target_input) # Convert the hostname/IP text into a valid IPv4 address
        except socket.gaierror: # Unless the hostname can't be resolved
          self.error_occurred.emit("Hostname could not be resolved.")
          return # Will no longer attempt to scan

        futures = []
        with ThreadPoolExecutor(max_workers=100) as executor: # Manages a pool of reusable worker threads, will run a maximum of 100 active threads (simultaneously)
            for port in range(1, 65536): # For the every port in the range of 1 to 65535 (the max for IPv4 TCP and UDP)
                futures.append(executor.submit(self.scan_port, target_ip, port)) # The futures list will let us see if a failure happened while running the code.
            for future in futures: # Goes back through every port we scanned.
                try:
                    future.result() # Waits for the specific ports scan to finish.
                except socket.error: 
                    pass

        self.finished_scan.emit()

class PortScanner(QWidget): # PortScanner will inherit from the parent of QWidget
    def __init__(self):
        super().__init__() # In case we have arguments to send to the parent, we call the super class.
        self.port_label = QLabel("Enter your target IP: ", self) # Our label for the port scanner.
        self.port_input = QLineEdit(self) # Our text box for the port scanner.
        self.results_list = QListWidget(self) # Our list for the results of the scanner.
        self.scan_button = QPushButton("Scan", self) # When we click on this button, we'll scan the target IP.
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Port Scanner") # Changes the title of our window.
        self.setGeometry(500, 200, 500, 600) # Sets the size of our window.

        vbox = QVBoxLayout() # Handles all of our widgets.
        vbox.addWidget(self.port_label)
        vbox.addWidget(self.port_input)
        vbox.addWidget(self.results_list) 
        vbox.addWidget(self.scan_button)

        self.setLayout(vbox)
        self.port_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop) # Sets the label to the top middle.

        self.port_label.setObjectName("port_label") # Changing the object names to apply styling.
        self.port_input.setObjectName("port_input")
        self.scan_button.setObjectName("scan_button")
        # Font and size customization for the GUI. Completely preference.
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#port_label{
                font-size: 40px;
            }
            QLineEdit#port_input{
                font-size: 40px;
                padding: 10px;
            }
            QPushButton#scan_button{
                font-size: 30px;
                font-weight: bold;
            }
    """) 
        self.scan_button.clicked.connect(self.start_scan) # When we click the button, it will run the start_scan method.

    def start_scan(self): # The method for starting the scan.
        target_input = self.port_input.text()
        self.results_list.clear()
        self.results_list.addItem(f"Scanning started at: {datetime.now()}") # Tells us when we started the scan.
        self.scan_button.setEnabled(False) # Will prevent double clicking mid scan.
        self.scan_button.setText("Scanning...") 

        self.thread = ScannerThread(target_input)
        self.thread.port_found.connect(self.add_result)
        self.thread.finished_scan.connect(self.scan_finished)
        self.thread.error_occurred.connect(self.scan_error)
        self.thread.start()

    def add_result(self, port): # The method to add the results to our GUI.
        self.results_list.addItem(f"Port {port} is open") # Tells us which ports are open.

    def scan_finished(self): # The method to reenable our scan button back to normal.
        self.results_list.addItem(f"Scan finished at: {datetime.now()}") # Tells us when we finished the scan.
        self.scan_button.setEnabled(True) # Lets us click on the button again.
        self.scan_button.setText("Scan") # Sets the button text back to "Scan"

    def scan_error(self, message): # The method for if there was an error scanning our target IP.
        self.results_list.addItem(message) # Our message if the scan fails.
        self.scan_button.setEnabled(True) # Lets us click on the button again.
        self.scan_button.setText("Scan") # Sets the button text back to "Scan"

def main():
    app = QApplication(sys.argv)
    window = PortScanner() # Our window object is equal to the constructor of our PortScanner()
    window.show() # Will make our port scanner show.
    sys.exit(app.exec_()) # This allows our window to stay open until we close it.

if __name__ == "__main__":
    main()