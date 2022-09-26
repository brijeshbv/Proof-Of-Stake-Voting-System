

from block import Block
from utils import BlockChainUtils

class BlockChain():
    

    def __init__(self) -> None:
        self.blocks = [Block.genesis()]
    
    def addBlock(self, block):
        if not self.lastBlockHashValid(block):
            print("last block hash is not valid")
            return
        if not self.blockCountValid(block):
            print("block count not valid")
            return
        self.blocks.append(block)
    
    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data
    

    def blockCountValid(self, block):
        """checks if new incoming block count is valid"""
        return self.blocks[-1].blockCount == block.blockCount -1
    
    def lastBlockHashValid(self, block):
        latestBlockChainBlockHash =  BlockChainUtils.hash(self.blocks[-1].payload()).hexdigest()

        return latestBlockChainBlockHash == block.lastHash

    