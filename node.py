from blockchain import BlockChain
from transaction_pool import TransactionPool
from utils import BlockChainUtils
from wallet import Wallet
from socket_communication import SocketCommunication
from node_api import NodeAPI
from message import Message
from utils import BlockChainUtils

class Node():

    def __init__(self, hostIP, port) -> None:
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockChain = BlockChain()
        self.hostIP = hostIP
        self.port = port
        self.p2p = None

    def startP2P(self):
        self.p2p = SocketCommunication(self.hostIP, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        senderPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, senderPublicKey)
        transactionExists = self.transactionPool.transactionExists(transaction)
        if not transactionExists and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)
            encodedMessage = BlockChainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)