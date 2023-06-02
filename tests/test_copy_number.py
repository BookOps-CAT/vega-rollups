import pytest

from pymarc import Field, Subfield

from copy_number import (
    complex_subfield_n,
    determine_subfield_n_position,
    find_digits,
    get_number,
    has_complex_subfields,
    has_single_subfield_n,
    normalize_value,
    modify_uniform_title,
)


@pytest.mark.parametrize("arg,expectation", [
        ("1 and 2", True),
        ("Volumne 3, part 1", True),
        ("Volume III, 1930-1935", True),
        ("Knigi 1 i 2", True),
        ("Volumes 1-2-3", True),
        ("Volumes 16, 17, 18", True),
        ("5 & 6", True),
        ("Part one", True),
        ("5", False),
        ("15", False),
        ("Book 3.", False),
        ("Vol. 5", False),
        ("Vol. 55 /", False),
        ("[Vol 45].", False)

    ])
def test_complex_subfield_n(arg, expectation):
    assert complex_subfield_n(arg) == expectation

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


def test_has_single_subfield_n_missing(stub_245_no_number):
    assert has_single_subfield_n(stub_245_no_number) is False

def test_has_single_subfield_n_present(stub_245_with_number):
    assert has_single_subfield_n(stub_245_with_number) is True

def test_has_single_subfield_n_multiple(stub_245_with_number):
    stub_245_with_number.subfields.append(Subfield("n", "9"))
    assert len(stub_245_with_number.get_subfields("n")) > 1
    assert has_single_subfield_n(stub_245_with_number) is False

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


def determine_subfield_n_position_if_no_sub_6(stub_240):
    assert determine_subfield_n_position(stub_240) == 1

def determine_subfield_n_position_if_sub_6_present(stub_240):
    stub_240.subfields.insert(0, Subfield("6", "spam"))

    assert determine_subfield_n_position(stub_240) == 2


def test_get_number_invalid_tag(stub_245_no_number):
    stub_245_no_number.tag = "246"

    with pytest.raises(ValueError):
        get_number(stub_245_no_number)


def test_get_number_no_subfield(stub_245_no_number):
    assert get_number(stub_245_no_number) is None


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("1", "1"),
        ("Book 3 /", "3"),
        ("Vol. 55 /", "55"),
        ("Chapter4 ", None),
        ("Chapter", None),
        ("Volumne 3, part 1", None),
        ("Volume III, 1930-1935", None),
        ("Knigi 1 i 2", None),
        ("Volumes 1-2-3", None)
    ],
)
def test_find_digits(arg, expectation):
    assert find_digits(arg) == expectation


def test_modify_uniform_title_missing_240(stub_245_with_number):
    with pytest.raises(ValueError):
        modify_uniform_title("5", stub_245_with_number)


def test_modify_uniform_title(stub_240):
    field = modify_uniform_title("5", stub_240)
    assert isinstance(field, Field) is True
    assert str(field) == "=240  10$aFoo.$n5.$lEnglish"


def test_modifify_uniform_title_when_subfield_6_present(stub_240):
    stub_240.subfields.insert(0, Subfield("6", "bar"))
    field = modify_uniform_title("5", stub_240)

    assert str(field) == "=240  10$6bar$aFoo.$n5.$lEnglish"


def test_modify_uniform_title_when_field_is_None():
    with pytest.raises(AttributeError):
        assert modify_uniform_title(5, None)


def test_modify_uniform_title_when_number_is_None(stub_240):
    assert modify_uniform_title(None, stub_240) is None
