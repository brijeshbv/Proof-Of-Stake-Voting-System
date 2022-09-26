import json
import uu
import uuid
import time
import copy
class Transaction():

    def __init__(self, senderPublicKey, receiverPublicKey, amount, type) -> None:
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''


    def toJson(self):
        return self.__dict__

    #adds signature to transaction.
    def addSign(self, signature):
        self.signature = signature

    
    def payload(self):
        """The signature is removed from a copy and returned. Useful for validating transactions"""
        jsonRep = copy.deepcopy(self.toJson())
        jsonRep['signature'] = ''
        return jsonRep


    def equals(self, transaction):
        return self.id == transaction.id