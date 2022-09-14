from transaction import Transaction

from wallet import Wallet

if __name__ == '__main__':
    sender = 'sender'
    receiver = 'receiver'
    amount = '2'
    type = 'TRANSFER'


    txn = Transaction(sender, receiver, amount, type)
    

    wallet = Wallet()
    signature = wallet.sign(txn.toJson())
    txn.sign(signature)
    print(txn.toJson())
