import hashlib

def merkle(transactions):
    if len(transactions) == 0:
        return ""
    if len(transactions) == 1:
        return hashlib.sha256(transactions[0].encode()).hexdigest()
    newMerkleTree = []
    for i in range(0, len(transactions), 2):
        t = transactions[i]
        if i + 1 < len(transactions):
            t += transactions[i + 1]
        newMerkleTree.append(hashlib.sha256(t.encode()).hexdigest())
    return merkle(newMerkleTree)

def transactions(n, p):
    prevBlockHash = "0000"
    for x in range((2**n) // (2**p)):
        transactions = []
        for i in range(2**p):
            message = input(f"Enter message for transaction {i+1} in block {x+1}: ")
            transactions.append(message)
        currRoot = prevBlockHash + merkle(transactions)
        currBlockHash = hashlib.sha256(currRoot.encode()).hexdigest()
        print(f"Block {x+1} : Hash Value = {currBlockHash}")
        print(f"Transactions in Block {x+1}: {transactions}\n")
        prevBlockHash = currBlockHash

# Example usage
# transactions(2, 1)

if __name__ == "__main__":
    n = int(input('Enter total number of transaction blocks (as exponent of 2): '))
    p = int(input('Enter number of transactions per block (as exponent of 2): '))
    transactions(n, p)