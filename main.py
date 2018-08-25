from compression.huffman import HuffmanCoding

# if __name__ == "__main__":
input_data = ''
with open("dickens.txt", errors="ignore") as f:
    input_data = f.read().strip()


h = HuffmanCoding(input_data)

compress = h.compress(input_data)
print(len(compress))
print(len(compress) / len(input_data))
decoded = h.decompress(compress)
print(decoded == input_data)


