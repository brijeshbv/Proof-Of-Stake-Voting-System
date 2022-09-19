from transaction import Transaction
from transaction_pool import TransactionPool

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

    signatureValid = wallet.signatureValid(txn.payload(),txn.signature, wallet.publicKeyString())
    
    pool.addTransaction(txn)
    print(pool.toJson())

