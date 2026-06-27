import os
import json
from pathlib import Path
from src.huffman import HuffmanCoding


class Compressor:

    def __init__(self):
        self.huffman = HuffmanCoding()

    ##################################################
    # READ FILE
    ##################################################

    def read_file(self, file_path):
        """
        Reads file in binary-safe mode.
        """
        with open(file_path, "rb") as f:
            return f.read().decode("utf-8", errors="ignore")

    ##################################################
    # WRITE BINARY FILE (BIT PACKING)
    ##################################################

    def write_binary_file(self, bit_string, output_path):
        """
        Converts bit string into real compressed binary file.
        """

        byte_array = bytearray()

        for i in range(0, len(bit_string), 8):
            byte = bit_string[i:i+8]

            # pad last byte
            if len(byte) < 8:
                byte = byte.ljust(8, "0")

            byte_array.append(int(byte, 2))

        with open(output_path, "wb") as f:
            f.write(bytes(byte_array))

    ##################################################
    # SAVE METADATA
    ##################################################

    def save_metadata(self, metadata_path, frequency):
        """
        Save frequency table for decompression.
        """

        with open(metadata_path, "w") as f:
            json.dump(frequency, f)

    ##################################################
    # MAIN COMPRESS FUNCTION
    ##################################################

    def compress_file(self, input_path, output_path="compressed.bin"):

        # Step 1: Read file
        text = self.read_file(input_path)

        # Step 2: Huffman compression
        encoded_text, frequency = self.huffman.compress(text)

        # Step 3: Write compressed binary file
        self.write_binary_file(encoded_text, output_path)

        # Step 4: Save metadata (VERY IMPORTANT for decompression)
        metadata_path = output_path + ".meta.json"
        self.save_metadata(metadata_path, frequency)

        # Step 5: Stats
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)

        ratio = compressed_size / original_size

        return {
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": round(ratio, 4),
            "output_file": output_path,
            "metadata_file": metadata_path
        }