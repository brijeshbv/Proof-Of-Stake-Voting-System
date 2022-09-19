from transaction import Transaction

from wallet import Wallet

if __name__ == '__main__':
    sender = 'sender'
    receiver = 'receiver'
    amount = '2'
    type = 'TRANSFER'
    # creates a wallet
    wallet = Wallet()
    txn = wallet.createTransaction(receiver, amount, type)

    signatureValid = wallet.signatureValid(txn.payload(),txn.signature, wallet.publicKeyString())
    print(txn.toJson(), signatureValid)

