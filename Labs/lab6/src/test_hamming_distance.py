import pytest

from hamming_distance import hamming_distance


def test_none_none():
    with pytest.raises(TypeError):
        hamming_distance(None, None)


def test_first_none():
    assert hamming_distance(None, "abc") == -1


def test_second_none():
    assert hamming_distance("abc", None) == -1


def test_different_length():
    with pytest.raises(ValueError):
        hamming_distance("abc", "abcd")


def test_empty_strings():
    assert hamming_distance("", "") == 0


def test_equal_strings():
    assert hamming_distance("father", "father") == 0


def test_one_difference():
    assert hamming_distance("pip", "pop") == 1


def test_two_differences():
    assert hamming_distance("abcd", "abab") == 2


def test_hello_hallo():
    assert hamming_distance("hello", "hallo") == 1


def test_all_different():
    assert hamming_distance("abcd", "efgi") == 4
