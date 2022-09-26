

class BlockChain():
    

    def __init__(self) -> None:
        self.blocks = []
    
    def addBlock(self, block):
        self.blocks.append(block)
    