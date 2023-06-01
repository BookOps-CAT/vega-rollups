import pytest

from pymarc import Field

from copy_number import (
    find_digits,
    get_number,
    has_complex_subfields,
    normalize_value,
    modify_uniform_title,
)


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("d", True),
        ("f", True),
        ("g", True),
        ("h", True),
        ("k", True),
        ("m", True),
        ("n", True),
        ("o", True),
        ("p", True),
        ("r", True),
        ("s", True),
        ("a", False),
        ("l", False),
    ],
)
def test_has_complex_subfields(arg, expectation):
    assert has_complex_subfields(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("abc", "abc"),
        ("abc3", "abc3"),
        (" abc ", "abc"),
        ("abc,", "abc"),
        ("abc;", "abc"),
        ("a b", "ab"),
        ("", ""),
        ("a-b./c", "abc"),
    ],
)
def test_normalize_value(arg, expectation):
    assert normalize_value(arg) == expectation


def test_get_number_invalid_tag(stub_title_no_number):
    stub_title_no_number.tag = "246"

    with pytest.raises(ValueError):
        get_number(stub_title_no_number)


def test_get_number_no_subfield(stub_title_no_number):
    assert (get_number(stub_title_no_number)) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("1", "1"),
        ("Book 3 /", "3"),
        ("Vol. 55 /", "55"),
        ("Chapter4 ", None),
        ("Chapter", None),
        ("Volumne 3, part 1", "3"),
    ],
)
def test_find_digits(arg, expectation):
    assert (find_digits(arg)) == expectation


def test_modify_uniform_title_missing_240(stub_title_with_number):
    with pytest.raises(ValueError):
        modify_uniform_title("5", stub_title_with_number)


def test_modify_uniform_title(stub_240):
    field = modify_uniform_title("5", stub_240, 1)
    print(field)
