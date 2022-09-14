from Crypto.Hash import SHA256
import json

class BlockChainUtils():

    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        databytes = dataString.encode('utf-8')
        dataHash = SHA256.new(databytes)
        return dataHash