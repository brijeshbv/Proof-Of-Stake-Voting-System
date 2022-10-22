

from block import Block
from consensus_factory import getConsensusStrategy
from proof_of_stake import ProofOfStake
from utils import BlockChainUtils
from accountmodel import AccountModel
from wallet import Wallet

class BlockChain():
    

    def __init__(self) -> None:
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.concensus = getConsensusStrategy('pos')
        

    def addBlock(self, block):
        """Add a new block to the block list"""
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
        """Validate the hash of the last block"""
        latestBlockChainBlockHash =  BlockChainUtils.hash(self.blocks[-1].payload()).hexdigest()

        return latestBlockChainBlockHash == block.lastHash

    def getCoveredTransactionSet(self, transactions):
        """Add transactions covered by the sender to coveredTransactions list and return that list"""
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction)
            else:
                print("Transaction is not covered by sender", transaction)
        return coveredTransactions

    def transactionCovered(self, transaction):
        """Check if a transaction is covered by sender"""
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
        """Execute block transaction and update the token balance of sender and receiver"""
        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:
                token = transaction.token
                self.concensus.update(sender, token)
                self.accountModel.updateBalance(sender, -token)
        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        token = transaction.token

        self.accountModel.updateBalance(sender, -token) #update sender's token balance (deduction)
        self.accountModel.updateBalance(receiver, token) #update receiver's token balance

    
    def nextForger(self):
        """Return the data hash of the last block"""
        lastBlockHash = BlockChainUtils.hash(self.blocks[-1].payload()).hexdigest()
        nextForger = self.concensus.forger(lastBlockHash)
        return nextForger


    def createBlock(self, transactionsFromPool, forgerWallet):
        """Create a new block in blockchain"""
        coveredTransactions = self.getCoveredTransactionSet(transactionsFromPool)
        self.executeTransactions(coveredTransactions)
        if len(coveredTransactions) > 0:
            newBlock = forgerWallet.createBlock(coveredTransactions, BlockChainUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))
            self.blocks.append(newBlock)
            print(f"created block  no {len(self.blocks)}")
            return newBlock
        return None
        
    def doesTransactionExist(self, transaction):
        """Check if a transaction already exists in the block's transactions list"""
        for block in self.blocks:
            for txn in block.transactions:
                if txn.equals(transaction):
                    return True
        return False
    
    def doesTransactionBetweenPartiesExist(self, senderPublicKey, receiverPublicKey):
        '''checks only if there is a past transaction between two parties'''
        print('len of blocks',len(self.blocks))
        for block in self.blocks:
            for txn in block.transactions:
                if txn.isBetweenSameParties(senderPublicKey, receiverPublicKey):
                    print('similar transactions found')
                    return True
        print('no similar transactions found')
        return False
    
    def forgerValid(self, block):
        """Check if a forger is valid by comparing the forger's public key with the proposed block's public key"""
        forgerPublicKey = self.concensus.forger(block.lastHash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        return False
    
    def transactionsValid(self, transactions):
        """Validate the transactions by comparing the item count in coveredTransactions list with the item count of proposed transactions list"""
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False

