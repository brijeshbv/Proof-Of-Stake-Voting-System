import copy
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
        ## ensure that transaction is not already in blockchain to avoid the case where broadcasted covered transaction in a block
        ## will be returned again through a broadcast and added back to transaction pool.
        if not isTransactionInBlockChain and not transactionExists and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)
            encodedMessage = BlockChainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
            forgerRequired = self.transactionPool.forgerRequired()
            if forgerRequired == True :
                self.forge()
    
    def handleBlock(self, block):
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature
        blockCountValid = self.blockChain.blockCountValid(block)
        lastBlockHashValid = self.blockChain.lastBlockHashValid(block)
        forgerValid = self.blockChain.forgerValid(block)
        transactionsValid = self.blockChain.transactionsValid(block.transactions)
        signatureValid = self.wallet.signatureValid(blockHash, signature, forger)
        if not blockCountValid :
            print("blockcount invalid, requesting for longer blockchains")
            self.requestChain()
        if lastBlockHashValid and forgerValid and transactionsValid and transactionsValid and signatureValid and blockCountValid:
            print("block added here 1")
            self.blockChain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK',block)
            encodedMessage = BlockChainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
        else:
            print("Block was invalid and not added to transaction",
             f'\nlastBlockHashValid: {lastBlockHashValid},forgerValid :{forgerValid}, transactionsValid: {transactionsValid}, transactionsValid: {transactionsValid}')

    def requestChain(self):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None )
        encodeMessage = BlockChainUtils.encode(message)
        self.p2p.broadcast(encodeMessage)

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
    
    def handleBlockChainRequest(self, connectedNode):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAIN', self.blockChain)
        encodedMessage = BlockChainUtils.encode(message)
        self.p2p.send(connectedNode, encodedMessage)

    def handleBlockChain(self, blockChain):
        localBlockChainCopy = copy.deepcopy(self.blockChain)
        localBlockChainCount = len(localBlockChainCopy.blocks)
        receivedBlockChainCount = len(blockChain.blocks)
        if localBlockChainCount < receivedBlockChainCount:
            for blockNumber, block in enumerate(blockChain.blocks):
                if blockNumber > localBlockChainCount:
                    print("block added here 2")
                    localBlockChainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockChain = localBlockChainCopy