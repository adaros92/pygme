import os
import pkg_resources
import sys


class Dictionary(object):

    def __init__(self, config: dict) -> None:
        self.dictionary_filename = config["dictionary_filename"]
        self.words = []
        self._load_dictionary()

    def _load_dictionary(self):
        directory_path = pkg_resources.resource_filename('pygme', 'data/')
        full_path = os.path.join(directory_path, self.dictionary_filename)
        with open(full_path, "r") as f:
            self.words = f.readlines()

    def get_random_word(self, min_length=0, max_length=sys.maxsize):
        eligible_words = []