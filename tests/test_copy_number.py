import pytest

from copy_number import get_number, find_digits, normalize_value


@pytest.mark.parametrize("arg,expectation", [
        ("abc", "abc"),
        ("abc3", "abc3"),
        (" abc ", "abc"),
        ("abc,", "abc"),
        ("abc;", "abc"),
    ])
def test_normalize_value(arg, expectation):
    assert normalize_value(arg) == expectation

def test_get_number_invalid_tag(stub_title_no_number):
    stub_title_no_number.tag = "246"
    
    with pytest.raises(ValueError):
        get_number(stub_title_no_number)


def test_get_number_no_subfield(stub_title_no_number):
    assert(get_number(stub_title_no_number)) is None


@pytest.mark.parametrize("arg,expectation", [
        ("1", "1"),
        ("Book 3 /", "3"),
        ("Vol. 55 /", "55"),
        ("Chapter4 ", None),
        ("Chapter", None),
        ("Volumne 3, part 1", "3")

    ])
def test_find_digits(arg, expectation):
    assert(find_digits(arg)) == expectation