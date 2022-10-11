from electoral_node import ElectoralNode
from node import Node
import sys

from node_api import NodeAPI

if __name__ == '__main__':
    
    # python run main.py <IP> <Port>
    hostIP = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])
    keyFile = None
    if len(sys.argv) > 4:
        keyFile = sys.argv[4]
    
 
    #initialize a node
    node = ElectoralNode(hostIP = hostIP, port=port, key=keyFile)
    node.startP2P()
    node.startAPI(apiPort, NodeAPI())
