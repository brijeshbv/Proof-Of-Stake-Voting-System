

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

    def removeFromPool(self, transactions):
        newPoolTransactions = []
        for poolTransactions in self.transactions:
            insert = True
            for transaction in transactions:
                if poolTransactions.equals(transaction):
                    insert = False
            if(insert == True):
                newPoolTransactions.append(poolTransactions)
        self.transactions = newPoolTransactions
