class FileService:
    def __init__(self, file_repo):
        self.file_repo = file_repo

    def find_all_files(self):
        return self.file_repo.find_all_files()

    def find_files_containing_substring(self, substring):
        all_files = self.file_repo.find_all_files()
        sorted_files = []
        for file in all_files:
            if substring in file.nume:
                sorted_files.append(file)
        return sorted_files

    def find_files_by_content_parts_text(self, text_content):
        files = self.file_repo.find_all_files()
        found_files = []
        for file in files:
            with open(file.path) as f:
                if text_content in f.read():
                    found_files.append(file)
        return found_files

    def find_files_by_content_parts_binary(self, binary_content):
        try:
            # convert from binary to text
            text_content = bytearray.fromhex(binary_content).decode()

            return self.find_files_by_content_parts_text(text_content)
        except ValueError:
            print("Invalid binary format")
            return []

    def find_files_with_duplicate_hash(self):
        files = self.file_repo.find_all_files_sorted_by_hash()
        duplicate_files = []
        i = 0
        while i < len(files) - 1:
            if files[i].hash == files[i + 1].hash:
                duplicate_files.append(files[i])
                i += 1
                while i < len(files) and files[i].hash == files[i - 1].hash:
                    duplicate_files.append(files[i])
                    i += 1
            else:
                i += 1
        return duplicate_files
