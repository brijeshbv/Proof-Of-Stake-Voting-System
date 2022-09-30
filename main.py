from node import Node
import sys

if __name__ == '__main__':
    
    # python run main.py <IP> <Port>
    hostIP = sys.argv[1]
    port = int(sys.argv[2])
 
    #initialize a node
    node = Node(hostIP = hostIP, port=port)
    node.startP2P()
