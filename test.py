

import string
from lot import Lot
from proof_of_stake import ProofOfStake
import random


def getRandomString(length):
    letters = string.ascii_lowercase
    resultString = ''.join(random.choice(letters) for i in range(length))
    return resultString

if __name__ == "__main__":
    pos = ProofOfStake()
    pos.update('bob',50)
    pos.update('alice',100)

    bobWins, aliceWins = 0, 0

    for i in range(100):
        forger = pos.forger(getRandomString(i))
        if forger == "bob":
            bobWins +=1
        elif forger == "alice": 
            aliceWins +=1

    print(bobWins, aliceWins)



