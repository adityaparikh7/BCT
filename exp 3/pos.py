import hashlib
import time
import random


class Validator:
    def __init__(self, id, stake):
        self.id = id
        self.stake = stake

    def __repr__(self):
        return f"Validator(id={self.id}, stake={self.stake})"


def select_validator(validators):
    total_stake = sum(v.stake for v in validators)
    pick = random.uniform(0, total_stake)
    current = 0
    for validator in validators:
        current += validator.stake
        if current > pick:
            return validator
    return validators[0]


def verify_block(block, previous_block_hash):
    if block.previous_hash != previous_block_hash:
        return False
    if block.hash != block.calculate_hash():
        return False
    return True


class Block:
    def __init__(self, index, previous_hash, timestamp, data, validator):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_contents = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.data) + self.validator.id
        return hashlib.sha256(block_contents.encode('utf-8')).hexdigest()


def main():
    num_validators = int(input("Enter the number of validators: "))
    validators = []

    for i in range(num_validators):
        validator_id = input(f"Enter the ID for validator {i + 1}: ")
        stake = int(input(f"Enter the number of coins to stake for Validator {validator_id}: "))
        validators.append(Validator(validator_id, stake))
    
    print(validators)

    num_blocks = int(input("Enter the number of blocks: "))
    previous_block_hash = "0" * 64  
    blockchain = []

    for i in range(num_blocks):
        num_transactions = int(input(f"Enter the number of transactions for block {i + 1}: "))
        transactions = [input(f"Enter transaction {j + 1}: ") for j in range(num_transactions)]

        selected_validator = select_validator(validators)
        block = Block(i + 1, previous_block_hash, time.time(), transactions, selected_validator)

        if verify_block(block, previous_block_hash):
            blockchain.append(block)
            previous_block_hash = block.hash
            print(f"Block {i + 1} is verified and is added to the blockchain by Validator {selected_validator.id}\n")
        else:
            print(f"Block {i + 1} verification failed. Block not added to the blockchain.\n")


if __name__ == "__main__":
    main()
