import sys
from io import StringIO


def main(args):
    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python lzw-decompress.py InputFile OutputFile")
    inputfile, outputfile = args

    # Perform file compression
    with open(inputfile, "rb") as f_in, open(outputfile, "w") as f_out:
        input_data = f_in.read().strip()
        decompressed = decompress(input_data)
        f_out.write(decompressed)


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    # Build the dictionary.
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()


# Main launcher
if __name__ == "__main__":
	main(sys.argv[1 : ])