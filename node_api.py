from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from utils import BlockChainUtils
from vote_utils.registered_candidates import Candidates

node = None

class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask( __name__)

    def start(self, apiPort):
        NodeAPI.register(self.app, route_base='/') #Register flaskview class with your flask app 
        self.app.run(host= 'localhost', port=apiPort)

    def injectNode(self, injectedNode):
        global node
        node = injectedNode

    @route('/info', methods=['GET'])
    def info(self):
        return 'This is a communication interface to a nodes blockchain', 200
    
    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        """Returns the entire blockchain in json format"""
        return node.blockChain.toJson(), 200

    @route('transactionPool', methods=['GET'])
    def transactionPool(self):
        """Returns the transaction pool in json format"""
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route('transaction', methods=['POST'])
    def transaction(self):
        """Performs transaction"""
        print("performing transaction")
        values = request.get_json()
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        transaction = BlockChainUtils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201
    


    @route('register', methods=['POST'])
    def registerVoter(self):
        """Registers the voter"""
        print("Registering voter")
        values = request.get_json()
        if not 'publicKey' in values:
            return 'Missing publicKey value', 400
        publicKey = BlockChainUtils.decode(values['publicKey'])
        node.handleRegistration(publicKey)
        response = {'message': 'Received registration request'}
        return jsonify(response), 201


    @route('/candidates',methods=['GET'])
    def getCandidates(self):
        """Returns the candidates public key and votes"""
        candidates = Candidates()
        candidateKeys = candidates.getResiteredCandidates()
        candidateDict = {}
        for i, candidate in enumerate(candidateKeys) :
            token = node.blockChain.accountModel.getBalance(candidate)
            candidateDict[i] = {
                'publicKey' : candidate,
                'votes': token,
            }
        return candidateDict, 200