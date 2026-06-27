import os
from src.compressor import Compressor
from src.decompressor import Decompressor


def print_menu():
    print("\n==============================")
    print(" Dynamic File Compression Tool")
    print("==============================")
    print("1. Compress File")
    print("2. Decompress File")
    print("3. Exit")
    print("==============================")


def compress_flow():
    compressor = Compressor()

    input_path = input("Enter input file path: ").strip()

    if not os.path.exists(input_path):
        print("❌ File not found!")
        return

    output_path = "compressed.bin"

    result = compressor.compress_file(input_path, output_path)

    print("\n✅ Compression Successful!")
    print(f"Original Size   : {result['original_size']} bytes")
    print(f"Compressed Size : {result['compressed_size']} bytes")
    print(f"Compression Ratio: {result['compression_ratio']}")
    print(f"Output File     : {result['output_file']}")
    print(f"Metadata File   : {result['metadata_file']}")


def decompress_flow():
    decompressor = Decompressor()

    input_path = input("Enter compressed file path: ").strip()
    metadata_path = input("Enter metadata file path: ").strip()
    output_path = "decompressed_output.txt"

    if not os.path.exists(input_path):
        print("❌ Compressed file not found!")
        return

    if not os.path.exists(metadata_path):
        print("❌ Metadata file not found!")
        return

    result = decompressor.decompress_file(
        input_path,
        metadata_path,
        output_path
    )

    print("\n✅ Decompression Successful!")
    print(f"Output File: {result['output_file']}")


def main():
    while True:
        print_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            compress_flow()

        elif choice == "2":
            decompress_flow()

        elif choice == "3":
            print("Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice! Try again.")


if __name__ == "__main__":
    main()