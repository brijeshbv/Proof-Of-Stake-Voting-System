from re import T
from Crypto.PublicKey import RSA
from transaction import Transaction
from utils import BlockChainUtils
from Crypto.Signature import PKCS1_v1_5

class Wallet():

    def __init__(self):
        self.keyPair = RSA.generate(2048)

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


    def createTransaction(self, receiverPublicKey, amount, type):
        transaction = Transaction(self.publicKeyString(),
        receiverPublicKey, 
        amount, 
        type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

