#Create a BlockChain

import datetime   # Timestamp
import hashlib    # To Hash the blocks
import json
from flask import Flask, jsonify

#Build a Blockchain

class Blockchain:

    def __init__(self):

        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
