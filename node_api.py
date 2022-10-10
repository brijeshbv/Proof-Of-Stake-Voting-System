from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from utils import BlockChainUtils

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
        return node.blockChain.toJson(), 200

    @route('transactionPool', methods=['GET'])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route('transaction', methods=['POST'])
    def transaction(self):
        print("performing transaction")
        values = request.get_json()
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        transaction = BlockChainUtils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201
    
    
    @route('register', methods=['POST'])
    def register(self):
        print("Registering voter")
        values = request.get_json()
        if not 'publicKey' in values:
            return 'Missing publicKey value', 400
        publicKey = BlockChainUtils.decode(values['publicKey'])
        node.handleRegistration(publicKey)
        response = {'message': 'Received registration request'}
        return jsonify(response), 201
    

    