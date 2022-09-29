from blockchain import BlockChain
from transaction import Transaction
from transaction_pool import TransactionPool
import pprint
from block import Block
from utils import BlockChainUtils
from wallet import Wallet
from accountmodel import AccountModel

if __name__ == '__main__':
    
    blockchain = BlockChain()
    pool = TransactionPool()

    alice = Wallet()
    bob = Wallet()
    exchange = Wallet()
    forger = Wallet()

    exchangeTransaction = exchange.createTransaction(alice.publicKeyString(), 10, "EXCHANGE")
    if not pool.transactionExists(exchangeTransaction):
        pool.addTransaction(exchangeTransaction)
    
    coveredTransactions = blockchain.getCoveredTransactionSet(pool.transactions)
    lastHash = BlockChainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
    blockCount = blockchain.blocks[-1].blockCount + 1
    blockOne = forger.createBlock(coveredTransactions, lastHash, blockCount)
    blockchain.addBlock(blockOne)
    
    #remove blockOne from transaction pool after adding the block to the blockchain inorder to avoid block duplication

    pool.removeFromPool(blockOne.transactions)  

    # alice wants to send 5 token to bob
    transaction = alice.createTransaction(bob.publicKeyString(), 5, 'TRANSFER')

    if not pool.transactionExists(transaction):
        pool.addTransaction(transaction)

    coveredTransactions = blockchain.getCoveredTransactionSet(pool.transactions)
    lastHash = BlockChainUtils.hash(blockchain.blocks[-1].payload()).hexdigest()
    blockCount = blockchain.blocks[-1].blockCount + 1
    blockTwo = forger.createBlock(coveredTransactions, lastHash, blockCount)
    blockchain.addBlock(blockTwo)

    #remove blockTwo from transaction pool after adding the block to blockchain
    pool.removeFromPool(blockTwo.transactions)  

    pprint.pprint(blockchain.toJson())