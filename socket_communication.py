import imp
from p2pnetwork.node import Node
from overrides import overrides

from peer_discovery_handler import PeerDiscoveryHandler

class SocketCommunication(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(SocketCommunication, self).__init__(host, port, id, callback, max_connections)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)

    
    def startSocketCommunication(self):
        self.start()
        self.peerDiscoveryHandler.start()

    @overrides
    def inbound_node_connected(self, node):
        print("inbound connection")
        self.send_to_node(node, "Hi I am responding to you")

    @overrides
    def outbound_node_connected(self, node):
        print("outbound node connected")
        self.send_to_node(node, "Hi I am trying to talk to you")

    def node_message(self, node, data):
        print(data)