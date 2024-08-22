from merkle_nonce import *
import time

class Block:
    def __init__(self, previous_hash, merkle_root, data):
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_contents = str(self.timestamp) + \
            self.previous_hash + self.merkle_root + str(self.data)
        return hash(block_contents)


# Creating a block
previous_block_hash = "0" * 64  # Example previous hash
block_data = ["Apple", "Google", "Samsung", "Microsoft"]
hashed_block_data = [hash(data) for data in block_data]
merkle_root = merkle(hashed_block_data)

block = Block(previous_block_hash, merkle_root, block_data)
print(f"Block Hash: {block.hash}")
print(f"Previous Hash: {block.previous_hash}")
print(f"Merkle Root: {block.merkle_root}")
print(f"Timestamp: {block.timestamp}")
print(f"Data: {block.data}")
