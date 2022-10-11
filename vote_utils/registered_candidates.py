
from Crypto.PublicKey import RSA


class Candidates():

    def getResiteredCandidates(self):
        candidates = [
                'keys/candidate1PublicKey.pem',
                'keys/candidate2PublicKey.pem',
                'keys/candidate3PublicKey.pem',
                'keys/candidate4PublicKey.pem',
                'keys/candidate5PublicKey.pem',
        ]
        registeredCandidates = []
        for candidate in candidates:
            f = open(candidate,'r')
            key = RSA.import_key(f.read())
            publicKey = key.public_key().export_key('PEM').decode('utf-8') 
            registeredCandidates.append(publicKey)
        return registeredCandidates



    
    