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


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0" * 64, time.time(), "Genesis Block", 1)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block()  # Mine the block before adding it
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i} has an invalid previous hash")
                return False

            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i} has an invalid hash")
                return False

        print("Blockchain is valid")
        return True

    # def modify_block_data(self, block_index, transaction_index, new_data):
    #     if block_index < 1 or block_index >= len(self.chain):
    #         print("Invalid block index.")
    #         return

    #     block = self.chain[block_index]
    #     if transaction_index < 0 or transaction_index >= len(block.data):
    #         print("Invalid transaction index.")
    #         return

    #     print(f"Original Data: {block.data[transaction_index]}")
    #     block.data[transaction_index] = new_data
    #     print(f"New Data: {block.data[transaction_index]}")

    #     # Re-mine the block since the data has changed
    #     print(f"Re-mining block {block_index}...")
    #     block.mine_block()

    #     # Ensure the next block points to the new hash
    #     if block_index < len(self.chain) - 1:
    #         self.chain[block_index + 1].previous_hash = block.hash


def main():
    blockchain = Blockchain()

    num_blocks = int(input("Enter the number of blocks: "))

    for i in range(1, num_blocks + 1):
        difficulty = int(input(f"Enter the difficulty level for block {i}: "))
        num_transactions = int(input(f"Enter the number of transactions for block {i}: "))
        transactions = [input(f"Enter transaction {j + 1}: ") for j in range(num_transactions)]

        new_block = Block(i, blockchain.get_latest_block().hash, time.time(), transactions, difficulty)
        start_time = datetime.datetime.now()
        blockchain.add_block(new_block)
        end_time = datetime.datetime.now()

        print(f"Block {i} has been added to the blockchain\n")
        print(f"Time taken: {end_time - start_time} seconds\n")

    print("Blockchain verification:")
    blockchain.is_chain_valid()

    # Option to modify block data
    # while True:
    #     modify = input("Do you want to modify any block data? (yes/no): ").lower()
    #     if modify == 'yes':
    #         block_index = int(input("Enter the block index to modify (1 to n): "))
    #         transaction_index = int(input(f"Enter the transaction index in block {block_index}: "))
    #         new_data = input("Enter the new data: ")

    #         blockchain.modify_block_data(block_index, transaction_index, new_data)

    #         print("\nBlockchain verification after modification:")
    #         blockchain.is_chain_valid()
    #     else:
    #         break

    print("\nBlockchain Data:")
    print("------------------------------------------------------------------------------")
    for block in blockchain.chain:
        print(f"Block {block.index}")
        print(f"Difficulty: {block.difficulty}\n")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Block Hash: {block.hash}")
        print(f"Data: {block.data}")
        print("\n")
        print("------------------------------------------------------------------------------")


if __name__ == "__main__":
    main()
