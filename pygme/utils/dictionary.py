import os
import pkg_resources
import random
import sys


class Dictionary(object):

    def __init__(self, config: dict) -> None:
        self.dictionary_filename = config["dictionary_filename"]
        self.words = []
        self._load_dictionary()

    def _load_dictionary(self):
        """ Reads the dictionary file specified in the config assumed to be stored in data subdirectory """
        directory_path = pkg_resources.resource_filename('pygme', 'data/')
        full_path = os.path.join(directory_path, self.dictionary_filename)
        with open(full_path, "r") as f:
            words = f.readlines()
        self.words = [word.strip("\n") for word in words]

    def get_random_word(self, min_length: int = 1, max_length: int = sys.maxsize) -> str:
        """ Retrieves a random word with length between the given minimum and max length arguments

        :param min_length - the minimum length that the word should have
        :param max_length - the maximum length that the word should have

        :returns a random word from the dictionary matching the given length criteria
        """
        eligible_words = [word for word in self.words if min_length <= len(word) <= max_length]
        return random.choice(eligible_words)
