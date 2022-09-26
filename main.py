from blockchain import BlockChain
from transaction import Transaction
from transaction_pool import TransactionPool
import pprint
from block import Block
from utils import BlockChainUtils
from wallet import Wallet

if __name__ == '__main__':
    sender = 'sender'
    receiver = 'receiver'
    amount = '2'
    type = 'TRANSFER'
    # creates a wallet
    wallet = Wallet()
    pool = TransactionPool()

    txn = wallet.createTransaction(receiver, amount, type)
    blockChain = BlockChain()
    
    pool.addTransaction(txn)

    lastHash = BlockChainUtils.hash(blockChain.blocks[-1].payload()).hexdigest()
    newBlockCount = blockChain.blocks[-1].blockCount + 1
    block = wallet.createBlock(pool.transactions,lastHash, newBlockCount)

    # add blocks to chain
    blockChain.addBlock(block)

    pprint.pprint(blockChain.toJson())