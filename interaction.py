from time import sleep
from turtle import pos
from wallet import Wallet
from utils import BlockChainUtils
import requests
from Crypto.PublicKey import RSA

def postTransaction(sender, receiverPublicKeyString, token, type):
    transaction = sender.createTransaction(receiverPublicKeyString, token, type)

    url = 'http://localhost:5002/transaction'
    package = {'transaction': BlockChainUtils.encode(transaction)}

    request = requests.post(url, json=package)
    print(request.text)



def postRegistration(sender):
    publicKey = sender.publicKeyString()
    url = 'http://localhost:5002/register'
    package = {'publicKey': BlockChainUtils.encode(publicKey)}

    request = requests.post(url, json=package)
    print(request.text)

def getPublicKey(file):
    return open(file,'r').read()

if __name__ == '__main__':
    
    alice = Wallet()
    alice.fromKey('keys/voter1PrivateKey.pem')
    postRegistration(alice)
    sleep(1)
    bobsKey = getPublicKey('keys/candidate1PrivateKey.pem')
    postTransaction(alice, bobsKey, 1, "TRANSFER")
    


    