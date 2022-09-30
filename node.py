from blockchain import BlockChain
from transaction_pool import TransactionPool
from wallet import Wallet
from socket_communication import SocketCommunication

class Node():

    def __init__(self, hostIP, port) -> None:
        self.transationPool = TransactionPool()
        self.wallet = Wallet()
        self.blockChain = BlockChain()
        self.hostIP = hostIP
        self.port = port
        self.p2p = None

    def startP2P(self):
        self.p2p = SocketCommunication(self.hostIP, self.port)
        self.p2p.startSocketCommunication()