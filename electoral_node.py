
from pprint import pprint
from node import Node
from vote_utils.registered_voters import Voters
from transaction import Transaction
class ElectoralNode(Node):
    NO_OF_VOTES = 5

    def __init__(self, hostIP, port, key=None) -> None:
        super().__init__(hostIP, port, key)

    def handleRegistration(self, publicKey):
        if Voters.isValidVoter(publicKey) == True:
            exchangeTransaction = self.wallet.createTransaction(publicKey,self.NO_OF_VOTES, 'EXCHANGE' )
            pprint(exchangeTransaction.payload())
            if self.handleTransaction(exchangeTransaction):
                print('registration added to transaction pool')

