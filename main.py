import os
from itertools import chain
from hashlib import sha256


class DuplicatesRemover(object):

    def __init__(self, search_path: str, file_type: str):
        self.path = search_path
        self.f_type = file_type

    def find_duplicates(self):
        file_paths = self.collect_file_paths()
        files_size = self.calcucalate_files_size(file_paths)
        files_with_identical_size = self. find_files_with_identical_size(files_size)
        files_hashes = self.calculate_file_hash(files_with_identical_size)

    def collect_file_paths(self):
        file_tree = os.walk(self.path)
        file_paths = []
        for root_dir, dirs, files in file_tree:
            for file_name in files:
                file_paths.append(f"{root_dir}/{file_name}")
        return file_paths

    @staticmethod
    def calcucalate_files_size(file_paths):
        return {file_path: os.path.getsize(file_path) for file_path in file_paths}

    def find_files_with_identical_size(self, files_size):
        """
        :param files_size: {file_path: file_size}
        rev_dict: {file_size1: {file1_path, file2_path}, file_size2: {file5_path, file12_path}...}
        :return set(file1_path, file2_path)
        """
        rev_dict = {}
        for f_path, f_size in files_size.items():
            rev_dict.setdefault(f_size, set()).add(f_path)
        result = set(chain.from_iterable(values for key, values in rev_dict.items() if len(values) > 1))
        return result

    @staticmethod
    def calculate_file_hash(files_path):
        result = {}
        for path in files_path:
            with open(path, "rb") as file:
                f_read = file.read()
                f_hash = sha256(f_read)
                result[path] = f_hash
        return result

