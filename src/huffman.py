"""
huffman.py
-----------

Core Huffman Coding implementation for Dynamic File Compression Utility.

This module provides:
1. Node class
2. Frequency table generation
3. Huffman tree construction
4. Huffman code generation
5. Encoding
6. Decoding
"""

import heapq
from collections import Counter


class HuffmanNode:
    """
    Node used in the Huffman Tree.
    """

    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """
        Required for heapq.
        Compares nodes by frequency.
        """
        return self.freq < other.freq


class HuffmanCoding:

    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}
        self.root = None

    ##################################################
    # STEP 1
    # Frequency Calculation
    ##################################################

    def calculate_frequency(self, text):
        """
        Returns dictionary of character frequencies.
        """

        return Counter(text)

    ##################################################
    # STEP 2
    # Build Min Heap
    ##################################################

    def build_heap(self, frequency):

        self.heap = []

        for character, freq in frequency.items():

            node = HuffmanNode(character, freq)

            heapq.heappush(self.heap, node)

    ##################################################
    # STEP 3
    # Merge Nodes
    ##################################################

    def merge_nodes(self):

        while len(self.heap) > 1:

            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = HuffmanNode(None, node1.freq + node2.freq)

            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

        self.root = self.heap[0]
        ##################################################
# STEP 4
# Generate Huffman Codes
##################################################

    def build_codes_helper(self, node, current_code):
        """
        Recursive function to generate Huffman codes.
        """

        if node is None:
            return

        # If leaf node → store the code
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char
            return

        # Traverse left → add "0"
        self.build_codes_helper(node.left, current_code + "0")

        # Traverse right → add "1"
        self.build_codes_helper(node.right, current_code + "1")


    def build_codes(self):
        """
        Initializes recursion for code generation.
        """

        self.codes = {}
        self.reverse_codes = {}

        if self.root is None:
            return

        self.build_codes_helper(self.root, "")

    ##################################################
    # STEP 5
    # Encode Text
    ##################################################

    def encode_text(self, text):
        """
        Converts input text into Huffman encoded binary string.
        """

        encoded_output = ""

        for char in text:
            encoded_output += self.codes[char]

        return encoded_output
    ##################################################
# STEP 6
# Decode Huffman Encoded String
##################################################

    def decode_text(self, encoded_text):
        """
        Converts Huffman encoded binary string back to original text.
        """

        decoded_output = ""
        current_code = ""

        for bit in encoded_text:
            current_code += bit

            if current_code in self.reverse_codes:
                character = self.reverse_codes[current_code]
                decoded_output += character
                current_code = ""

        return decoded_output


##################################################
# STEP 7
# FULL PIPELINE FUNCTIONS
##################################################

    def compress(self, text):
        """
        Full compression pipeline:
        text → frequency → heap → tree → codes → encoded text
        """

        frequency = self.calculate_frequency(text)
        self.build_heap(frequency)
        self.merge_nodes()
        self.build_codes()

        encoded_text = self.encode_text(text)

        return encoded_text, frequency


    def decompress(self, encoded_text):
        """
        Full decompression pipeline using existing tree.
        """

        return self.decode_text(encoded_text)


##################################################
# STEP 8
# Utility Debug Function
##################################################

    def show_codes(self):
        """
        Prints Huffman codes (for learning/debugging).
        """

        print("\nHuffman Codes:")
        for char, code in self.codes.items():
            print(f"{repr(char)} : {code}")