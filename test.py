from interaction import getPublicKey, postRegistration
from interaction import postTransaction
from wallet import Wallet
from time import sleep
import sys



class Test():


    def testProofOfStake(self):
        node1 = Wallet()
        node1.fromKey('keys/stakerPrivateKey.pem')
        postRegistration(node1)
        sleep(1)
        postTransaction(node1, node1.publicKeyString(), 5, "STAKE")


    def testTransaction(self):
        voter1 = Wallet()
        voter1.fromKey('keys/voter1PrivateKey.pem')
        postRegistration(voter1)
        voter2 = Wallet()
        voter2.fromKey('keys/voter2PrivateKey.pem')
        postRegistration(voter2)
        sleep(1)
        candidate1Key = getPublicKey('keys/candidate1PublicKey.pem')
        postTransaction(voter1, candidate1Key, 1, "TRANSFER")
        candidate2Key = getPublicKey('keys/candidate2PublicKey.pem')
        postTransaction(voter1, candidate2Key, 3, "TRANSFER")
        sleep(1)
        candidate3Key = getPublicKey('keys/candidate3PublicKey.pem')
        postTransaction(voter1, candidate3Key, 1, "TRANSFER")
        postTransaction(voter2, candidate2Key, 4, "TRANSFER")

    def testOverVoting(self):
        voter1 = Wallet()
        voter1.fromKey('keys/voter1PrivateKey.pem')
        candidate1Key = getPublicKey('keys/candidate1PublicKey.pem')
        postTransaction(voter1, candidate1Key, 1, "TRANSFER")

    def testMultipleRegistration(self):
        voter1 = Wallet()
        voter1.fromKey('keys/voter1PrivateKey.pem')
        postRegistration(voter1)
        


if __name__ == "__main__":
    testInstance = Test()
    testNo = sys.argv[1]
    if testNo == '1':
        testInstance.testProofOfStake()
    elif testNo == '2':
        testInstance.testTransaction()
    elif testNo == '3':
        testInstance.testOverVoting()
    elif testNo == '4':
        testInstance.testMultipleRegistration()


