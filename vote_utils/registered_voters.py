from Crypto.PublicKey import RSA

from blockchain import BlockChainUtils

class Voters():

    @staticmethod
    def getRegisteredVoters():
        return [
            'keys/voter1PublicKey.pem',
            'keys/voter2PublicKey.pem',
            'keys/voter3PublicKey.pem',
            'keys/voter4PublicKey.pem',
            'keys/voter5PublicKey.pem',
            'keys/voter6PublicKey.pem',
            'keys/voter7PublicKey.pem',
            'keys/voter8PublicKey.pem',
            'keys/voter9PublicKey.pem',
            'keys/stakerPublicKey.pem',
        ]

    @staticmethod
    def isValidVoter(publicKey):
        for voterKeyFile in Voters().getRegisteredVoters():
            f = open(voterKeyFile,'r')
            key = RSA.import_key(f.read())
            if key.public_key().export_key('PEM').decode('utf-8') == publicKey:
                return True
            f.close()
        return False

