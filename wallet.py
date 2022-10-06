from re import T
from Crypto.PublicKey import RSA
from block import Block
from transaction import Transaction
from utils import BlockChainUtils
from Crypto.Signature import PKCS1_v1_5

class Wallet():

    def __init__(self):
        self.keyPair = RSA.generate(2048)
    
    
    def fromKey(self, file):
        '''assigns a predefined public key to a wallet.'''
        key = ''
        with open(file, 'r') as keyFile:
            key = RSA.importKey(keyFile.read())
        self.keyPair = key

    def sign(self, data):
        datahash = BlockChainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(datahash)
        return signature.hex()
    
    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = BlockChainUtils.hash(data)
        publicKey = RSA.import_key(publicKeyString)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)
        signatureValid = signatureSchemeObject.verify(dataHash, signature)
        return signatureValid

    def publicKeyString(self):
        return self.keyPair.public_key().export_key('PEM').decode('utf-8')


    def createTransaction(self, receiverPublicKey, token, type):
        transaction = Transaction(self.publicKeyString(),
        receiverPublicKey, 
        token, 
        type)
        signature = self.sign(transaction.payload())
        transaction.addSign(signature)
        return transaction

    def createBlock(self, transactions, lastHash, blockCount):
        block = Block(transactions, lastHash, self.publicKeyString(), blockCount)
        signature = self.sign(block.payload())
        block.addSign(signature)
        return block