import hashlib
import time
import random
from ecdsa import SigningKey, VerifyingKey, NIST384p  # ECDSA for signing


class UTXO:
    def __init__(self, amount, recipient):
        self.amount = amount
        self.recipient = recipient


class Transaction:
    def __init__(self, sender_public_key, recipient, amount, utxos, fee=0):
        self.sender_public_key = sender_public_key
        self.recipient = recipient
        self.amount = amount
        self.utxos = utxos  # List of UTXOs being spent
        self.fee = fee
        self.signature = None

    def calculate_hash(self):
        transaction_contents = f"{self.sender_public_key}{self.recipient}{self.amount}{self.utxos}{self.fee}"
        return hashlib.sha256(transaction_contents.encode('utf-8')).hexdigest()

    def sign_transaction(self, private_key):
        if self.calculate_total_input() < self.amount + self.fee:
            raise ValueError("Not enough UTXOs to cover transaction")
        self.signature = private_key.sign(
            self.calculate_hash().encode('utf-8'))

    def verify_signature(self):
        if not self.signature:
            raise ValueError("Transaction not signed")
        verifying_key = VerifyingKey.from_string(
            bytes.fromhex(self.sender_public_key), curve=NIST384p)
        return verifying_key.verify(self.signature, self.calculate_hash().encode('utf-8'))

    def calculate_total_input(self):
        return sum(utxo.amount for utxo in self.utxos)

    def __repr__(self):
        return f"Tx {self.calculate_hash()} - from {self.sender_public_key[:10]}... to {self.recipient[:10]}... for {self.amount} with fee {self.fee}"


class Block:
    def __init__(self, index, previous_hash, timestamp, transaction, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transaction = transaction
        self.difficulty = difficulty
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_contents = f"{self.index}{self.previous_hash}{self.timestamp}{self.transaction}{self.nonce}"
        return hashlib.sha256(block_contents.encode('utf-8')).hexdigest()

    def mine_block(self):
        target = '0' * self.difficulty
        start_time = time.time()
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        end_time = time.time()
        print(f"\nBlock {self.index} mined with hash: {self.hash}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Transaction: {self.transaction}")
        print(f"Time taken to mine: {end_time - start_time:.2f} seconds")


class Blockchain:
    def __init__(self, difficulty):
        self.difficulty = difficulty  # User-driven difficulty
        self.chain = [self.create_genesis_block()]
        self.utxo_pool = []  # Centralized UTXO pool
        self.pending_transactions = []

    def create_genesis_block(self):
        genesis_transaction = Transaction("0", "genesis", 50, [], fee=0)
        return Block(0, "0" * 64, time.time(), genesis_transaction, self.difficulty)

    def get_latest_block(self):
        return self.chain[-1]

    def create_utxo(self, recipient, amount):
        return UTXO(amount, recipient)

    def add_transaction(self, transaction):
        if not transaction.verify_signature():
            raise ValueError("Invalid transaction signature")
        self.pending_transactions.append(transaction)
        print(f"\nAdded transaction: {transaction}")

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            print("\nNo transactions to mine.")
            return False

        # Only process one transaction per block
        tx = self.pending_transactions.pop(0)
        block = Block(len(self.chain), self.get_latest_block().hash,
                      time.time(), tx, self.difficulty)
        block.mine_block()
        self.chain.append(block)

        # Update UTXO pool by removing spent UTXOs and adding new ones
        for utxo in tx.utxos:
            self.utxo_pool.remove(utxo)
        self.utxo_pool.append(self.create_utxo(
            tx.recipient, tx.amount - tx.fee))

        # Miner collects the transaction fee from the UTXO pool
        self.utxo_pool.append(self.create_utxo(miner_address, tx.fee))

        self.display_blockchain()

    def get_balance(self, address):
        balance = sum(
            utxo.amount for utxo in self.utxo_pool if utxo.recipient == address)
        return balance

    def generate_random_transaction(self, sender_keypair, recipient_address, amount, fee=1):
        sender_public_key = sender_keypair[0].to_string().hex()

        available_utxos = [
            utxo for utxo in self.utxo_pool if utxo.recipient == sender_public_key]
        if sum(utxo.amount for utxo in available_utxos) < amount + fee:
            print(f"Not enough balance to send {amount}")
            return

        tx = Transaction(sender_public_key, recipient_address,
                         amount, available_utxos, fee)
        tx.sign_transaction(sender_keypair[1])
        self.add_transaction(tx)
        return tx

    def display_blockchain(self):
        print("\n--- Blockchain Status ---")
        for block in self.chain:
            print(f"\nBlock {block.index}:")
            print(f"  Hash: {block.hash}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Transaction: {block.transaction}")
            print(
                f"  Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
        print("\n--- End of Blockchain ---")

# Crypto functions: key generation, signing, verification


def generate_keypair():
    private_key = SigningKey.generate(curve=NIST384p)
    public_key = private_key.get_verifying_key()
    return public_key, private_key


def main():
    # User-driven difficulty
    difficulty = int(input("Enter the mining difficulty (e.g., 1-5): "))

    # Create a blockchain with no new currency creation (reward comes from fees)
    blockchain = Blockchain(difficulty=difficulty)

    # Generate wallets (keypairs)
    wallet_a_keypair = generate_keypair()
    wallet_b_keypair = generate_keypair()

    # Initial UTXO pool for wallet A (currency exists from the start)
    blockchain.utxo_pool.append(blockchain.create_utxo(
        wallet_a_keypair[0].to_string().hex(), 100))

    # Interactive menu
    while True:
        print("\n--- Blockchain Menu ---")
        print("1. Create Transaction")
        print("2. Mine Transactions")
        print("3. Check Wallet Balance")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Create a transaction
            sender = wallet_a_keypair if input(
                "Send from wallet A? (y/n): ").lower() == 'y' else wallet_b_keypair
            recipient = wallet_b_keypair[0].to_string().hex(
            ) if sender == wallet_a_keypair else wallet_a_keypair[0].to_string().hex()
            amount = int(input("Enter the amount to send: "))
            fee = int(input("Enter the transaction fee: "))
            blockchain.generate_random_transaction(
                sender, recipient, amount, fee)

        elif choice == "2":
            # Mine pending transactions
            miner_address = wallet_a_keypair[0].to_string().hex() if input(
                "Mine to wallet A? (y/n): ").lower() == 'y' else wallet_b_keypair[0].to_string().hex()
            blockchain.mine_pending_transactions(miner_address)

        elif choice == "3":
            # Check balance
            address = wallet_a_keypair[0].to_string().hex() if input(
                "Check balance of wallet A? (y/n): ").lower() == 'y' else wallet_b_keypair[0].to_string().hex()
            print(f"Balance: {blockchain.get_balance(address)}")

        elif choice == "4":
            # Exit
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
