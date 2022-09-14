import uu
import uuid
import time

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