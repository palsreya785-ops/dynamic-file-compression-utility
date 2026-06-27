import json
from src.huffman import HuffmanCoding


class Decompressor:

    def __init__(self):
        self.huffman = HuffmanCoding()

    ##################################################
    # READ BINARY FILE
    ##################################################

    def read_binary_file(self, file_path):
        """
        Reads compressed binary file and converts it to bit string.
        """

        with open(file_path, "rb") as f:
            byte_data = f.read()

        bit_string = ""

        for byte in byte_data:
            bits = bin(byte)[2:].rjust(8, "0")
            bit_string += bits

        return bit_string

    ##################################################
    # LOAD FREQUENCY TABLE
    ##################################################

    def load_metadata(self, metadata_path):
        """
        Loads frequency table used to rebuild Huffman tree.
        """

        with open(metadata_path, "r") as f:
            return json.load(f)

    ##################################################
    # REBUILD HUFFMAN TREE
    ##################################################

    def rebuild_tree(self, frequency):
        """
        Reconstruct Huffman tree using frequency table.
        """

        self.huffman.build_heap(frequency)
        self.huffman.merge_nodes()
        self.huffman.build_codes()

    ##################################################
    # MAIN DECOMPRESSION FUNCTION
    ##################################################

    def decompress_file(self, input_path, metadata_path, output_path):

        # Step 1: Read bitstream
        bit_string = self.read_binary_file(input_path)

        # Step 2: Load frequency table
        frequency = self.load_metadata(metadata_path)

        # Step 3: Rebuild Huffman tree
        self.rebuild_tree(frequency)

        # Step 4: Decode bit string
        decoded_text = self.huffman.decode_text(bit_string)

        # Step 5: Write original file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decoded_text)

        return {
            "output_file": output_path,
            "status": "success",
            "original_size": len(decoded_text)
        }