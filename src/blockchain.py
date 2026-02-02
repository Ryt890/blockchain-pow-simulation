import hashlib
import time

class Block:
    def __init__(self, data, previous_hash, nonce, hash, timestamp):
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash
        self.time = timestamp

    def calculate_hash(self):
        content = self.data + self.previous_hash + str(self.nonce) + str(self.time)
        hash = hashlib.sha256(content.encode()).hexdigest()
        return hash
    
    
class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = int(input("Difficulty: "))
        self.max_block = int(input("Number of blocks: "))
        print(f"\n--------------------\n")
        genesis_block = self.create_genesis_block()
        self.chain.append(genesis_block)
        for i in range(1, self.max_block + 1):
            self.add_block(f"block {i}")
        


    def hash_block(self, data, previous_hash, nonce, timestamp):
        content = data + previous_hash + str(nonce) + str(timestamp)
        hash = hashlib.sha256(content.encode()).hexdigest()
        return hash

    def create_genesis_block(self):
        genesis = self.mine_block("genesis", "0")
        return Block("genesis", "0", genesis["nonce"], genesis["hash"], genesis["timestamp"])
    
    def mine_block(self, data, previous_hash):
        nonce = 0
        attempts = 0
        target = '0' * self.difficulty
        start_time = time.time()
        timestamp = time.time()
        while True: 
            hash = self.hash_block(data, previous_hash, nonce, timestamp)
            if hash.startswith(target):
                break
            nonce += 1
            attempts += 1
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        result = {
            "nonce": nonce,
            "hash": hash,
            "timestamp":  timestamp,
            "elapsed_time": elapsed_time,
            "attempts": attempts
        }
        return result        

    
    def add_block(self, data):
        previous_hash = self.chain[-1].hash
        mine_result = self.mine_block(data, previous_hash)
        block_number = len(self.chain)
        nonce = mine_result["nonce"]
        hash = mine_result["hash"]
        timestamp = mine_result["timestamp"]
        elapsed_time = mine_result["elapsed_time"]
        attempts = mine_result["attempts"]
        new_block = Block(data, previous_hash, nonce, hash, timestamp)
        self.chain.append(new_block)

        print(f"[Block {block_number} mined]\ndata: {data}\nnonce: {nonce}\nhash: {hash}\ntimestamp: {time.ctime(timestamp)}\ntime: {elapsed_time}\nattempts: {attempts}\n")
        print(f"--------------------\n")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]#現在のBlock
            previous_block = self.chain[i-1]#一つ前のBlock
            if current_block.previous_hash == previous_block.hash:

                if (previous_block.time <= current_block.time) and (current_block.time <= previous_block.time + 100):
                    
                    if current_block.hash == current_block.calculate_hash():
                        target = '0' * self.difficulty

                        if current_block.calculate_hash().startswith(target):
                            continue
                        else:
                             return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        return True
            
bc = Blockchain()
print("initial chain valid?:", bc.is_chain_valid())