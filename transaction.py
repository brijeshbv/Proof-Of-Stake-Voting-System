import json
import uu
import uuid
import time
import copy
class Transaction():

    def __init__(self, senderPublicKey, receiverPublicKey, token, type) -> None:
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.token = token
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''


    def toJson(self):
        return self.__dict__

    def addSign(self, signature):
        """Adds signature to transaction"""
        self.signature = signature

    
    def payload(self):
        """The signature is removed from a copy and returned. Useful for validating transactions"""
        jsonRep = copy.deepcopy(self.toJson())
        jsonRep['signature'] = ''
        return jsonRep


    def equals(self, transaction):
        """Compares the transaction id"""
        return self.id == transaction.id

    def isBetweenSameParties(self, sender , receiver):
        return self.senderPublicKey == sender and self.receiverPublicKey == receiver