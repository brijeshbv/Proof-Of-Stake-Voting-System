<<<<<<< HEAD
import copy
=======
>>>>>>> 5c8a6600ccd3861d36b8c0784ae38585d5061319
import time

class Block():

    def __init__(self, transactions, lastHash, forger, blockCount) -> None:
        self.transactions = transactions
        self.lastHash = lastHash
        self.forger = forger
        self.blockCount = blockCount
        self.timestamp = time.time()
        self.signature = ''
    
    def toJson(self):
        data = {}
        data['lastHash'] = self.lastHash
        data['forger'] = self.forger
        data['timestamp'] = self.timestamp
        data['blockCount'] = self.blockCount
        data['signature'] = self.signature
        jsonTxns = []
        for txn in self.transactions :
            jsonTxns.append(txn.toJson())
        data['transactions'] = jsonTxns
        return data

    def payload(self):
        jsonRep = copy.deepcopy(self.toJson())
        jsonRep["signature"] = ""
        return jsonRep
    
    def addSign(self, signature):
        self.signature = signature

