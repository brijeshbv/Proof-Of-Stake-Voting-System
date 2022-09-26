from transaction import Transaction
from transaction_pool import TransactionPool
import pprint
from block import Block
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

    
    pool.addTransaction(txn)

    block = wallet.createBlock(pool.transactions,'lastHash',1)

    pprint.pprint(block.toJson())

    signatureValid = Wallet.signatureValid(block.payload(),block.signature,wallet.publicKeyString())
    print(signatureValid)