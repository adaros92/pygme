import pytest
import random

from pygme.utils import dictionary


def test_word_assignment():
    """ Tests __setattr__ method of utils.dictionary.Word class """
    # The constructor will always convert the given word to lowercase
    word_object = dictionary.Word("Hello")
    assert word_object.word == "hello"
    # Word attribute should always be lower case
    word_object.word = "Hi"
    assert word_object.word == "hi"
    # Other attributes will be assigned normally
    word_object.some_other_attr = "Yo"
    assert word_object.some_other_attr == "Yo"


def test_word_contains():
    """ Tests __contains__ method of utils.dictionary.Word class """
    word_object = dictionary.Word("Hello")
    assert "l" in word_object and "L" in word_object
    assert "n" not in word_object and "N" not in word_object


def test_word_representation():
    """ Tests repr and str methods of utils.dictionary.Word class """
    word_object = dictionary.Word("Hello")
    assert repr(word_object) == str(word_object) and repr(word_object) == "hello"
    word_object = dictionary.Word("hello", show_only={"E", "o"})
    assert repr(word_object) == str(word_object) and repr(word_object) == "_e__o"


def test_word_length():
    """ Tests __len__ method of utils.dictionary.Word class """
    for word in ["Hello", "hi", "testing", "a"]:
        word_object = dictionary.Word(word)
        assert len(word_object) == len(word)


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
