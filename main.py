from transaction import Transaction

if __name__ == '__main__':
    sender = 'sender'
    receiver = 'receiver'
    amount = '2'
    type = 'TRANSFER'


    txn = Transaction(sender, receiver, amount, type)
    print(txn.toJson())