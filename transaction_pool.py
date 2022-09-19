

class TransactionPool():

    def __init__(self) -> None:
        self.transactions = []

    def addTransaction(self, transaction):
        if self.transactionExists(transaction) == False:
            self.transactions.append(transaction)

    def transactionExists(self, transaction):
        for txn in self.transactions:
            if txn.equals(transaction):
                return True
        return False

    def toJson(self):
        return self.__dict__