

from block import Block
from utils import BlockChainUtils
from accountmodel import AccountModel

class BlockChain():
    

    def __init__(self) -> None:
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
    
    def addBlock(self, block):
        if not self.lastBlockHashValid(block):
            print("last block hash is not valid")
            return
        if not self.blockCountValid(block):
            print("block count not valid")
            return
        self.executeTransactions(block.transactions)
        self.blocks.append(block)
    
    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data
    

    def blockCountValid(self, block):
        """checks if new incoming block count is valid"""
        return self.blocks[-1].blockCount == block.blockCount -1
    
    def lastBlockHashValid(self, block):
        latestBlockChainBlockHash =  BlockChainUtils.hash(self.blocks[-1].payload()).hexdigest()

        return latestBlockChainBlockHash == block.lastHash

    def getCoveredTransactionSet(self, transactions):
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction)
            else:
                print("Transaction is not covered by sender")
        return coveredTransactions

    def transactionCovered(self, transaction):
        if transaction.type == "EXCHANGE":
            return True
        senderBalance = self.accountModel.getBalance(transaction.senderPublicKey)
        if senderBalance >= transaction.amount:
            return True
        else:
            return False

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        amount = transaction.amount

        self.accountModel.updateBalance(sender, -amount) #update sender's account balance (deduction)
        self.accountModel.updateBalance(receiver, amount) #update receiver's account balance