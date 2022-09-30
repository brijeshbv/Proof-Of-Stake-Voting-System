import threading
import time
class PeerDiscoveryHandler():

    def __init__(self, node) -> None:
        self.socketCommunication = node

    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discover, args=())
        discoveryThread.start()

    def discover(self):
        while True:
            print("discovering")
            time.sleep(10)
    
    def status(self):
        while True:
            print("status")
            time.sleep(10)