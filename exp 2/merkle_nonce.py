import hashlib

def hash_nonce(data, nonce):
    return hashlib.sha256((data + str(nonce)).encode('utf-8')).hexdigest()

def merkle(blocks):
    if len(blocks) == 1:
        return blocks[0]
    new_blocks = []
    for i in range(0, len(blocks), 2):
        if i + 1 < len(blocks):
            new_blocks.append(hash_nonce(
                blocks[i], i) + hash_nonce(blocks[i + 1], i + 1))
        else:
            new_blocks.append(hash_nonce(
                blocks[i], i) + hash_nonce(blocks[i], i))
    return merkle(new_blocks)


data_blocks = ["Apple", "Google", "Samsung", "Microsoft"]
hash_blocks = [hash_nonce(data, i) for i, data in enumerate(data_blocks)]

print("Data Blocks:")
for i in range(len(data_blocks)):
    print(f"Block {i}: {data_blocks[i]}")
print("Hash Blocks:")
for i in range(len(hash_blocks)):
    print(f"Block {i}: {hash_blocks[i]}")
merkle_root = merkle(hash_blocks)
print(f"Merkle Root: {merkle_root}")
# print nonce value
