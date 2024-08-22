import hashlib
import time
import random


class Block:
  def __init__(self, timestamp, transactions, previous_hash=''):
    self.timestamp = timestamp
    self.transactions = transactions
    self.previous_hash = previous_hash
    self.hash = self.calculate_hash()
    self.nonce = 0

  def calculate_hash(self):
    sha = hashlib.sha256()
    sha.update(str(self.timestamp).encode('utf-8') +
               str(self.transactions).encode('utf-8') +
               str(self.previous_hash).encode('utf-8') +
               str(self.nonce).encode('utf-8'))
    return sha.hexdigest()

  def mine_block(self, difficulty):
    target = '0' * difficulty
    while self.hash[:difficulty] != target:
      self.nonce += 1
      self.hash = self.calculate_hash()
    print("Block mined:", self.hash)


class Validator:
  def __init__(self, name, stake):
    self.name = name
    self.stake = stake

  def __repr__(self):
    return f"Validator(name='{self.name}', stake={self.stake})"


def select_validator(validators):
  total_stake = sum([v.stake for v in validators])
  random_point = random.uniform(0, total_stake)
  current_stake = 0
  for validator in validators:
    current_stake += validator.stake
    if random_point <= current_stake:
      return validator


# User input
difficulty = int(input("Enter difficulty level (1-5): "))
num_blocks = int(input("Enter number of blocks: "))
num_transactions = int(input("Enter number of transactions per block: "))

# Proof of Work
print("\n--- Proof of Work ---")
blockchain = [Block(time.time(), ['Genesis Transaction'])]

for i in range(num_blocks):
  transactions = [f'Transaction {j+1}' for j in range(num_transactions)]
  new_block = Block(time.time(), transactions, blockchain[-1].hash)
  new_block.mine_block(difficulty)
  blockchain.append(new_block)

# Proof of Stake
print("\n--- Proof of Stake ---")
validators = [
    Validator('Alice', 100),
    Validator('Bob', 200),
    Validator('Charlie', 300)
]

blockchain = [Block(time.time(), ['Genesis Transaction'])]

for i in range(num_blocks):
  transactions = [f'Transaction {j+1}' for j in range(num_transactions)]
  selected_validator = select_validator(validators)
  print(f"Block {i+1} forged by: {selected_validator}")
  new_block = Block(time.time(), transactions, blockchain[-1].hash)
  blockchain.append(new_block)
