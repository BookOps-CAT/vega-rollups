import pytest

from pymarc import Field, Record, Subfield


@pytest.fixture
def stub_245_no_number():
    return Field(
        tag="245",
        indicators=["1", "0"],
        subfields=[
            Subfield(code="a", value="Foo /"),
            Subfield(code="c", value="Spam."),
        ],
    )


@pytest.fixture
def stub_245_with_number():
    return Field(
        tag="245",
        indicators=["1", "0"],
        subfields=[
            Subfield(code="a", value="Foo :"),
            Subfield(code="b", value="bar."),
            Subfield(code="n", value="Book 3 /"),
            Subfield(code="c", value="by John Smith."),
        ],
    )


@pytest.fixture
def stub_240():
    return Field(
        tag="240",
        indicators=["1", "0"],
        subfields=[
            Subfield(code="a", value="Foo."),
            Subfield(code="l", value="English"),
        ],
    )
