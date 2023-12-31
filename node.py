import copy
from pprint import pprint
from blockchain import BlockChain
from transaction_pool import TransactionPool
from utils import BlockChainUtils
from wallet import Wallet
from socket_communication import SocketCommunication
from node_api import NodeAPI
from message import Message
from utils import BlockChainUtils
import json
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

    def startAPI(self, apiPort, api):
        self.api = api
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        """Handles transaction"""
        print("handling transaction")
        data = transaction.payload()
        signature = transaction.signature
        senderPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, senderPublicKey)
        transactionExists = self.transactionPool.transactionExists(transaction)
        isTransactionInBlockChain = self.blockChain.doesTransactionExist(transaction)
        print('signature valid', signatureValid, transactionExists, isTransactionInBlockChain)
        if transaction.type == 'EXCHANGE':
            ## Exchange transactions are only permitted by genesis node
            genesisPubicKey = open('keys/genesisPublicKey.pem','r').read()
            isExchangeSignatureValid = Wallet.signatureValid(data, signature,genesisPubicKey )
            if not isExchangeSignatureValid:
                print('Exchange transaction from non-genesis node not permitted')
                return False
            else:
                print('Exchange transaction permitted')
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
            return True
        
        print("transaction not added to pool")
        return False
    
    def handleBlock(self, block):
        """Validates the block, adds the block to the blockchain, 
        removes the block from the block's transaction pool 
        and broadcasts a message to peers to notify them about the newly added block"""
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
        """Creates the next forger"""
        forger = self.blockChain.nextForger()
        if forger == self.wallet.publicKeyString():
            print("I am the next forger")
            newBlock = self.blockChain.createBlock(self.transactionPool.transactions, self.wallet)
            if newBlock != None:
                self.saveBlockChain()
                self.transactionPool.removeFromPool(self.transactionPool.transactions)
                message = Message(self.p2p.socketConnector, 'BLOCK',newBlock)
                encodedMessage = BlockChainUtils.encode(message)
                self.p2p.broadcast(encodedMessage)
        else:
            print("I am not the next forger")
    
    def handleBlockChainRequest(self, connectedNode):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAIN', self.blockChain)
        encodedMessage = BlockChainUtils.encode(message)
        print("sending blockchain to node", connectedNode)
        self.p2p.send(connectedNode, encodedMessage)

    def handleBlockChain(self, blockChain):
        localBlockChainCopy = copy.deepcopy(self.blockChain)
        localBlockChainCount = len(localBlockChainCopy.blocks)
        receivedBlockChainCount = len(blockChain.blocks)
        if localBlockChainCount < receivedBlockChainCount:
            print(f'local {localBlockChainCount}, receivedBlockChainCount {receivedBlockChainCount}')
            for blockNumber, block in enumerate(blockChain.blocks):
                if blockNumber >= localBlockChainCount :
                    localBlockChainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockChain = localBlockChainCopy
        
    def saveBlockChain(self):
        print('saving blockchain')
        genesisKey = open('keys/genesisPublicKey.pem','r').read()
        if self.wallet.publicKeyString() == genesisKey:
            with open("blockchain.json", "w") as outfile:
                json.dump(self.blockChain.toJson(), outfile)