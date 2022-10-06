from p2pnetwork.node import Node
from overrides import overrides
import json
from peer_discovery_handler import PeerDiscoveryHandler
from socket_connector import SocketConnector
from utils import BlockChainUtils

CENTRAL_NODE = 10001
class SocketCommunication(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(SocketCommunication, self).__init__(host, port, id, callback, max_connections)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(host, port)
        
        
    def connectToFirstNode(self):
        if self.socketConnector.port != CENTRAL_NODE:
             self.connect_with_node('localhost',CENTRAL_NODE)
    
    def startSocketCommunication(self, node):
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()

    @overrides
    def inbound_node_connected(self, node):
        self.peerDiscoveryHandler.handshake(node)

    @overrides
    def outbound_node_connected(self, node):
        self.peerDiscoveryHandler.handshake(node)

    def node_message(self, node, data):
        decodedMessage = BlockChainUtils.decode(json.dumps(data))
        if decodedMessage.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(decodedMessage)
        elif decodedMessage.messageType == 'TRANSACTION':
            transaction = decodedMessage.data
            self.node.handleTransaction(transaction)
        elif decodedMessage.messageType == 'BLOCK':
            block = decodedMessage.data
            self.node.handleBlock(block)
        elif decodedMessage.messageType == 'BLOCKCHAINREQUEST':
            self.node.handleBlockChainRequest(node)
        elif decodedMessage.messageType == 'BLOCKCHAIN':
            print("receieved a particular blockchain from node: ",node )
            blockChain = decodedMessage.data
            self.node.handleBlockChain(blockChain)


    def send(self, receiver, message):
        self.send_to_node(receiver, message)
    
    def broadcast(self, message):
        self.send_to_nodes(message)