
import threading
import time
from utils import BlockChainUtils
from message import Message
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
            handShakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handShakeMessage)
            time.sleep(10)
    
    def status(self):
        while True:
            print("Current Connections")
            for peer in self.socketCommunication.peers:
                print(str(peer.ip)+ ":" + str(peer.port))
            time.sleep(10)

    def handshake(self, connect_node):
        handShakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connect_node, handShakeMessage)

    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data = ownPeers
        messageType = 'DISCOVERY'
        message = Message(ownConnector, messageType, data)
        encodedMessage =  BlockChainUtils.encode(message)
        return encodedMessage

    def handleMessage(self, message):
        peerSocketConnector = message.senderConnector
        peersPeerList = message.data
        newPeer = True
        for peer in self.socketCommunication.peers:
            if peer.equals(peerSocketConnector):
                newPeer = False
        if newPeer == True:
            self.socketCommunication.peers.append(peerSocketConnector)
        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown= True
            if not peerKnown  and not peersPeer.equals(self.socketCommunication.socketConnector):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)


