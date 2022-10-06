
from utils import BlockChainUtils

class Lot():
    def __init__(self, publicKey,iteration, lastBlockHash ) -> None:
        self.publicKey = str(publicKey)
        self.iteration = iteration
        self.lastBlockHash = lastBlockHash

    def lotHash(self):
        hashData = self.publicKey + self.lastBlockHash
        for _ in range(self.iteration):
            hashData = BlockChainUtils.hash(hashData).hexdigest()
        return hashData