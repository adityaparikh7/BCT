import hashlib

def getNonce(string):
    nonce = 0
    while True:
        new_string = string + str(nonce)
        result = hashlib.sha256(new_string.encode("utf-8"))
        if result.hexdigest()[0:4] == "0000":
            return result.hexdigest(), nonce
        nonce += 1


def merkle(transactions):
    merkleTree = [hashlib.sha256(str(tx).encode()).hexdigest()for tx in transactions]
    while len(merkleTree) > 1:
        if len(merkleTree) % 2 != 0:
            merkleTree.append(merkleTree[-1])  
        newMerkleTree = []
        for i in range(0, len(merkleTree), 2):
            t = merkleTree[i] + merkleTree[i + 1]
            newMerkleTree.append(hashlib.sha256(str(t).encode()).hexdigest())
        merkleTree = newMerkleTree
    return merkleTree[0]


def transactions(n, p):
    prevBlockHash = "0000"
    for x in range((2**n) // (2**p)):
        transactions = []
        for i in range(2**p):
            message = input(f"Enter message for transaction {i+1} in block {x+1}: ")
            transactions.append(message)
        currRoot = prevBlockHash + merkle(transactions)
        currBlockHash, nonce = getNonce(currRoot)
        print(f"Block {x+1} : Hash Value = {currBlockHash}, Nonce = {nonce}")
        print(f"Transactions in Block {x+1}: {transactions}\n")
        prevBlockHash = currBlockHash


if __name__ == "__main__":
    n = int(input('Enter total number of transaction blocks (as exponent of 2): '))
    p = int(input('Enter number of transactions per block (as exponent of 2): '))
    transactions(n, p)

# def transactions(block_data):
#     prevBlockHash = "0000"
#     for x, block_transactions in enumerate(block_data):
#         currRoot = prevBlockHash + merkle(block_transactions)
#         currBlockHash, nonce = getNonce(currRoot)
#         print(f"Block {x+1} : Hash Value = {currBlockHash}, Nonce = {nonce}")
#         print(f"Transactions in Block {x+1}: {block_transactions}\n")
#         prevBlockHash = currBlockHash


# if __name__ == "__main__":
#     block_data = [
#         ["7.81", "6.95"],
#         ["6", "7.14"],
#         ["6.61", "7.84"]
#     ]
#     transactions(block_data)