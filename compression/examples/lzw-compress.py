import sys
from io import StringIO


def main(args):
    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python lzw-compress.py InputFile OutputFile")
    inputfile, outputfile = args

    # Perform file compression
    with open(inputfile, "r") as f_in, open(outputfile, "wb") as f_out:
        input_data = f_in.read().strip()
        compressed = compress(input_data)
        f_out.write(compressed)

def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result



# Main launcher
if __name__ == "__main__":
	main(sys.argv[1 : ])