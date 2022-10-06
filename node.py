from email import message
from blockchain import BlockChain
from transaction_pool import TransactionPool
from utils import BlockChainUtils
from wallet import Wallet
from socket_communication import SocketCommunication
from node_api import NodeAPI
from message import Message
from utils import BlockChainUtils

class Node():

    def __init__(self, hostIP, port, key = None) -> None:
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockChain = BlockChain()
        self.hostIP = hostIP
        self.port = port
        self.p2p = None
        if key is not None:
            self.wallet.fromKey(key)

    def startP2P(self):
        self.p2p = SocketCommunication(self.hostIP, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        print("handling transaction")
        data = transaction.payload()
        signature = transaction.signature
        senderPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, senderPublicKey)
        transactionExists = self.transactionPool.transactionExists(transaction)
        isTransactionInBlockChain = self.blockChain.doesTransactionExist(transaction)
        print(isTransactionInBlockChain)
        if not isTransactionInBlockChain and not transactionExists and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)
            encodedMessage = BlockChainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
            forgerRequired = self.transactionPool.forgerRequired()
            if forgerRequired == True :
                self.forge()
    
    def forge(self):
        forger = self.blockChain.nextForger()
        if forger == self.wallet.publicKeyString():
            print("I am the next forger")
            newBlock = self.blockChain.createBlock(self.transactionPool.transactions, self.wallet)
            self.transactionPool.removeFromPool(newBlock.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK',newBlock)
            encodedMessage = BlockChainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
        else:
            print("I am not the next forger")
    