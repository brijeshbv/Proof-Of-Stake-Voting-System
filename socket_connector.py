

class SocketConnector():
    
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port

    def equals(self, connector):
        return connector.ip == self.ip and connector.port == self.port