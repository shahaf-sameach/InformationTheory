import sys

from compression.huffman import HuffmanCoding


def main(args):
    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python huffman-compress.py InputFile OutputFile")
    inputfile, outputfile = args

    # Perform file compression
    with open(inputfile, "rb") as f_in, open(outputfile, "wb") as f_out:
        input_data = f_in.read().strip()
        h = HuffmanCoding(input_data)
        compressed = h.compress(input_data)
        f_out.write(compressed)
        # decoded = h.decompress(compressed)


# Main launcher
if __name__ == "__main__":
	main(sys.argv[1 : ])

