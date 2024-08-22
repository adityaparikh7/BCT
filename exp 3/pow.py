import hashlib
import time
import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_contents = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.data) + str(self.nonce)
        return hashlib.sha256(block_contents.encode('utf-8')).hexdigest()

    def mine_block(self):
        target = '0' * self.difficulty
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")


def chain_verify(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.previous_hash != previous_block.hash:
            print(f"Block {i} has an invalid previous hash")
            return False

        if current_block.hash != current_block.calculate_hash():
            print(f"Block {i} has an invalid hash")
            return False

    print("Blockchain is valid")
    return True

def main():
    # difficulty = int(input("Enter the difficulty level: "))
    num_blocks = int(input("Enter the number of blocks: "))

    previous_block_hash = "0" * 64 
    blockchain = []

    
    for i in range(num_blocks):
        difficulty = int(input("Enter the difficulty level: "))
        num_transactions = int(input(f"Enter the number of transactions for block {i + 1}: "))
        transactions = [input(f"Enter transaction {j + 1}: ") for j in range(num_transactions)]
        block = Block(i + 1, previous_block_hash,time.time(), transactions, difficulty)
        start_time = datetime.datetime.now()
        block.mine_block()
        end_time = datetime.datetime.now()
        blockchain.append(block)
        previous_block_hash = block.hash
        print(f"Block {i + 1} has been added to the blockchain\n")
        print(f"Time taken: {end_time - start_time} seconds\n")

    print("Blockchain verification:")
    chain_verify(blockchain)

    
    print("Blockchain Data:")
    print("------------------------------------------------------------------------------")
    for block in blockchain:
        print(f"Block {block.index}")
        print(f"Difficulty: {block.difficulty}\n")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Data: {block.data}")
        print("\n")
        print("------------------------------------------------------------------------------")
        # print(f"Timestamp: {block.timestamp}")
if __name__ == "__main__":
    main()
