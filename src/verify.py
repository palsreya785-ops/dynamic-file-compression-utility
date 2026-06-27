class Verifier:

    def normalize(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().replace("\r\n", "\n").strip()

    def compare_files(self, file1, file2):
        return self.normalize(file1) == self.normalize(file2)


if __name__ == "__main__":
    v = Verifier()

    if v.compare_files("sample.txt", "decompressed_output.txt"):
        print("✅ Verification Successful: Files match!")
    else:
        print("❌ Verification Failed")