from Crypto.PublicKey import RSA
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