
from node import Node
from voters.registered_voters import Voters

class ElectoralNode(Node):

    def __init__(self, hostIP, port, key=None) -> None:
        super().__init__(hostIP, port, key)

    def handleRegistration(publicKey):
        if Voters.isValidVoter(publicKey) == True:
            print('registration success')
