import hashlib

def hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def merkle(blocks):
    if len(blocks) == 1:
        return blocks[0]
    new_blocks = []
    for i in range(0, len(blocks), 2):
        if i + 1 < len(blocks):
            new_blocks.append(hash(blocks[i] + blocks[i + 1]))
        else:
            new_blocks.append(hash(blocks[i] + blocks[i]))
    return merkle(new_blocks)


data_blocks = ["Apple", "Google", "Samsung", "Microsoft"]
hash_blocks = [hash(data) for data in data_blocks]


print("Data Blocks:")
for i in range(len(data_blocks)):
    print(f"Block {i}: {data_blocks[i]}")
print("Hash Blocks:")
for i in range(len(hash_blocks)):
    print(f"Block {i}: {hash_blocks[i]}")
merkle_root = merkle(hash_blocks)
print(f"Merkle Root:{merkle_root}")










# print(verify_merkle(hash_blocks, merkle_root))
# def verify_merkle(root, data):
#     current = data
#     for i in range(len(root)):
#         if current == root[i]:
#             return True
#         current = hash(current + root[i])
#     return False
