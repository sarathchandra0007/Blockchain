#Create a BlockChain

import datetime   # Timestamp
import hashlib    # To Hash the blocks
import json       # Convert dict to string
from flask import Flask, jsonify

#Build a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')   # Genesis Block (First)

    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash}
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):            #A number minors need to execute to find proof, to attach created block to blockchain
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() #string of 64 characters are generated
            # A valid hash must have four leading zeros #0000
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()    #Make dict to string we use json dumps
        return hashlib.sha256(encoded_block).hexdigest()

    # Check whether previous block hash is same previous_hash of present block and check whether mining is done correctly or not
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


app=Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block = blockchain.get_last_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message' : 'You just mined the block, your block will add to blockchin',
                'index' : block['index'], 'timestamp': block['timestamp'],
                'proof' : block['proof'], 'previous_hash' : block['previous_hash']}
    
    return jsonify(response), 200

