import pytest
import random

from pygme.utils import dictionary


def test_load_dictionary():
    """ Tests _load_dictionary method of utils.dictionary.Dictionary class """
    dictionary_object = dictionary.Dictionary(pytest.default_dictionary_config)
    dictionary_object._load_dictionary()
    assert len(dictionary_object.words) > 0


def test_get_random_word():
    """ Tests get_random_word method of utils.dictionary.Dictionary class """
    dictionary_object = dictionary.Dictionary(pytest.default_dictionary_config)
    for _ in range(pytest.large_iteration_count):
        minimum_word_length = random.randint(1, 4)
        maximum_word_length = random.randint(minimum_word_length, minimum_word_length + 3)
        word = dictionary_object.get_random_word(minimum_word_length, maximum_word_length)
        assert minimum_word_length <= len(word) <= maximum_word_length
