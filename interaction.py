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

def postRegistration(sender):
    publicKey = sender.publicKeyString()
    url = 'http://localhost:5000/register'
    package = {'publicKey': BlockChainUtils.encode(publicKey)}

    request = requests.post(url, json=package)
    print(request.text)

if __name__ == '__main__':
    
    alice = Wallet()
    alice.fromKey('keys/voter1PrivateKey.pem')
    postRegistration(alice)
    sleep(1)
    bob = Wallet()
    bob.fromKey('keys/candidate1PrivateKey.pem')
    postTransaction(alice, bob, 1, "TRANSFER")
    


    