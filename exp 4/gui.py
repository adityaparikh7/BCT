import hashlib
import time
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext


class Block:
    def __init__(self, index, previous_hash, timestamp, data, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.mining_duration = 0

    def calculate_hash(self):
        block_contents = str(self.index) + self.previous_hash + \
            str(self.timestamp) + str(self.data) + str(self.nonce)
        return hashlib.sha256(block_contents.encode('utf-8')).hexdigest()

    def mine_block(self):
        target = '0' * self.difficulty
        start_time = time.time() 
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        end_time = time.time()
        self.mining_duration = end_time - start_time
        print(f"Block mined: {self.hash} in {self.mining_duration:.2f} seconds")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0" * 64, time.time(), "Genesis Block", 1)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                return False

            if current_block.hash != current_block.calculate_hash():
                return False

        return True


class BlockchainApp:
    def __init__(self, root):
        self.blockchain = Blockchain()
        self.root = root
        self.root.title("Blockchain Visualization")

        self.add_block_button = tk.Button(
            root, text="Add Block", command=self.add_block)
        self.add_block_button.pack(pady=10)

        self.validate_button = tk.Button(
            root, text="Validate Blockchain", command=self.validate_blockchain)
        self.validate_button.pack(pady=10)

        self.blockchain_display = scrolledtext.ScrolledText(
            root, width=100, height=60)
        self.blockchain_display.pack(pady=10)
        self.display_blockchain()

    def add_block(self):
        difficulty = simpledialog.askinteger(
            "Input", "Enter the difficulty level:", parent=self.root, minvalue=1, maxvalue=6)
        if difficulty is None:
            return

        num_transactions = simpledialog.askinteger(
            "Input", "Enter the number of transactions for the new block:", parent=self.root, minvalue=1)
        if num_transactions is None:
            return

        transactions = []
        for i in range(num_transactions):
            transaction = simpledialog.askstring(
                "Input", f"Enter transaction {i + 1}:", parent=self.root)
            if transaction:
                transactions.append(transaction)

        new_block = Block(len(self.blockchain.chain), self.blockchain.get_latest_block(
        ).hash, time.time(), transactions, difficulty)
        self.blockchain.add_block(new_block)
        self.display_blockchain()

    def validate_blockchain(self):
        if self.blockchain.is_chain_valid():
            messagebox.showinfo("Validation", "Blockchain is valid.")
        else:
            messagebox.showerror("Validation", "Blockchain is not valid.")

    def display_blockchain(self):
        self.blockchain_display.delete(1.0, tk.END)
        for block in self.blockchain.chain:
            block_info = f"Block {block.index}\n" \
                         f"Difficulty: {block.difficulty}\n" \
                         f"Nonce: {block.nonce}\n" \
                         f"Hash: {block.hash}\n" \
                         f"Previous Hash: {block.previous_hash}\n" \
                         f"Data: {block.data}\n" \
                         f"Timestamp: {datetime.datetime.fromtimestamp(block.timestamp)}\n" \
                         f"Mining Duration: {block.mining_duration:.2f} seconds\n"
            self.blockchain_display.insert(
                tk.END, block_info + "\n" + "-"*100 + "\n")


def main():
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
