import pytest
from longest_word import longest_word  # Adjust the import path as necessary

@pytest.fixture
def create_temp_file(tmp_path):
    def _create_temp_file(content):
        temp_file = tmp_path / "temp_file.txt"
        temp_file.write_text(content)
        return temp_file
    return _create_temp_file

def test_longest_word_single_longest(create_temp_file):
    content = "This is a test file with some words"
    temp_file = create_temp_file(content)
    assert longest_word(str(temp_file)) == "words"

def test_longest_word_multiple_longest_same_length(create_temp_file):
    content = "Each word here has four"
    temp_file = create_temp_file(content)
    # Assuming your function returns the first occurrence of the longest word
    assert longest_word(str(temp_file)) == "Each"

def test_longest_word_with_punctuation(create_temp_file):
    content = "Does it handle, punctuation?"
    temp_file = create_temp_file(content)
    # Depending on whether your function considers punctuation as part of a word, adjust the expected outcome
    assert longest_word(str(temp_file)) == "punctuation?"  # or "punctuation" if you strip punctuation

def test_longest_word_with_newlines(create_temp_file):
    content = "Word\nAnother\nLongestWord\nShort"
    temp_file = create_temp_file(content)
    assert longest_word(str(temp_file)) == "LongestWord"

def test_longest_word_empty_file(create_temp_file):
    content = ""
    temp_file = create_temp_file(content)
    assert longest_word(str(temp_file)) == ""
