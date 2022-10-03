
from lot import Lot
from utils import BlockChainUtils

class ProofOfStake():

    def __init__(self) -> None:
        self.stakers = {}

    def update(self, publicKeystring, stake):
        if publicKeystring in self.stakers.keys():
            self.stakers[publicKeystring] += stake
        else: 
            self.stakers[publicKeystring] = stake
    

    def getStake(self, publicKeystring):
        if publicKeystring in self.stakers.keys():
            return self.stakers[publicKeystring]
        else:
            print("This staker is not in the list of registered stakers.")
            return None
    
    def validatorLots(self, seed):
        lots = []
        for validator in self.stakers.keys():
            for stake in range(self.getStake(validator)):
                lots.append(Lot(validator, stake+1,seed))
        return lots


    def winnerLot(self ,lots, seed):
        winnerLot = None
        leastOffSet = None
        referenceHashIntegerValue = int(BlockChainUtils.hash(seed).hexdigest(), 16)
        for lot in lots:
            lotIntValue = int(lot.lotHash(), 16)
            offSet = abs(lotIntValue - referenceHashIntegerValue)
            if leastOffSet is None or offSet < leastOffSet :
                leastOffSet = offSet
                winnerLot = lot
        print(f'the winner lot was {winnerLot.publicKey}')
        return winnerLot

    def forger(self, lastBlockHash):
        lots = self.validatorLots(lastBlockHash)
        winnerLot = self.winnerLot(lots,lastBlockHash)
        return winnerLot.publicKey
