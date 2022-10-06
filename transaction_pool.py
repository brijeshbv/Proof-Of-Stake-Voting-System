

BLOCK_SIZE = int(1)
class TransactionPool():

    def __init__(self) -> None:
        self.transactions = []

    def addTransaction(self, transaction):
        if self.transactionExists(transaction) == True:
            print("Transaction already exists, can't add transaction")
            return
        print("transaction added to pool")
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

    def forgerRequired(self):
        print(len(self.transactions), "length")
        required = len(self.transactions) >= BLOCK_SIZE
        print("required?", required)
        return required

