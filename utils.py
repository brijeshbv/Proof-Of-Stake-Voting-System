
from Crypto.Hash import SHA256
import json
import jsonpickle
from Crypto.PublicKey import RSA

class BlockChainUtils():

    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        databytes = dataString.encode('utf-8')
        dataHash = SHA256.new(databytes)
        return dataHash

    
    @staticmethod
    def encode(objectToEncode):
        return jsonpickle.encode(objectToEncode, unpicklable=True)


    @staticmethod
    def decode(messageToDecode):
        return jsonpickle.decode(messageToDecode)

    
    @staticmethod
    def generateRSAPrivatePublicKeyPair():
        return RSA.generate(2048)



if __name__ == "__main__":

    for i in range(1,6):
        blk = BlockChainUtils.generateRSAPrivatePublicKeyPair()
        f = open(f'keys/candidate{i}PrivateKey.pem','wb')
        f.write(blk.export_key('PEM'))
        f.close()
        f = open(f'keys/candidate{i}PublicKey.pem','wb')
        f.write(blk.public_key().export_key('PEM'))
        f.close()
        
    for i in range(1,11):
        blk = BlockChainUtils.generateRSAPrivatePublicKeyPair()
        f = open(f'keys/voter{i}PrivateKey.pem','wb')
        f.write(blk.export_key('PEM'))
        f.close()
        f = open(f'keys/voter{i}PublicKey.pem','wb')
        f.write(blk.public_key().export_key('PEM'))
        f.close()

