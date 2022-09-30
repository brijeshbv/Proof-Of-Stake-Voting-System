from os import stat
from Crypto.Hash import SHA256
import json
import jsonpickle

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