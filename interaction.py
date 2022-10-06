from time import sleep
from turtle import pos
from wallet import Wallet
from utils import BlockChainUtils
import requests


def postTransaction(sender, receiver, token, type):
    transaction = sender.createTransaction(receiver.publicKeyString(), token, type)

    url = 'http://localhost:5000/transaction'
    package = {'transaction': BlockChainUtils.encode(transaction)}

    request = requests.post(url, json=package)
    print(request.text)

if __name__ == '__main__':
    bob = Wallet()
    alice = Wallet()
    alice.fromKey('keys/stakerPrivateKey.pem')
    exchange = Wallet()

    postTransaction(exchange, alice, 100, 'EXCHANGE')
    sleep(0.25)
    postTransaction(alice, alice, 25, 'STAKE')
    sleep(1)
    postTransaction(alice, bob, 1, 'TRANSFER')

    