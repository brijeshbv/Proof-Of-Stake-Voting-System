from Crypto.PublicKey import RSA


class Wallet():

    def __init__(self):
        self.keyPair = RSA.generate(2048)

