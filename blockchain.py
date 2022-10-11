

from block import Block
from proof_of_stake import ProofOfStake
from utils import BlockChainUtils
from accountmodel import AccountModel
from wallet import Wallet

class BlockChain():
    

    def __init__(self, nodeWallet) -> None:
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake()
        ## wallet associated with node that maintains dynamic instance of blockchain
        self.nodeWallet = nodeWallet
        

    def addBlock(self, block):
        self.executeTransactions(block.transactions)
        if self.blocks[-1].blockCount < block.blockCount:
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
        print(f"have: {self.blocks[-1].blockCount}, got {block.blockCount}")
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
                print("Transaction is not covered by sender", transaction)
        return coveredTransactions

    def transactionCovered(self, transaction):
        if transaction.type == "EXCHANGE":
            return True
        senderBalance = self.accountModel.getBalance(transaction.senderPublicKey)
        print('insufficient funds',senderBalance, transaction.token)
        if senderBalance >= transaction.token:
            return True
        else:
            return False

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:
                token = transaction.token
                self.pos.update(sender, token)
                self.accountModel.updateBalance(sender, -token)
        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        token = transaction.token

        self.accountModel.updateBalance(sender, -token) #update sender's token balance (deduction)
        self.accountModel.updateBalance(receiver, token) #update receiver's token balance

    
    def nextForger(self):
        lastBlockHash = BlockChainUtils.hash(self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger


    def createBlock(self, transactionsFromPool, forgerWallet):
        coveredTransactions = self.getCoveredTransactionSet(transactionsFromPool)
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(coveredTransactions, BlockChainUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))
        self.blocks.append(newBlock)
        print(f"created block  no {len(self.blocks)}")
        return newBlock
        
    def doesTransactionExist(self, transaction):
        for block in self.blocks:
            for txn in block.transactions:
                if txn.equals(transaction):
                    return True
        return False
    
    def forgerValid(self, block):
        forgerPublicKey = self.pos.forger(block.lastHash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        return False
    
    def transactionsValid(self, transactions):
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False

