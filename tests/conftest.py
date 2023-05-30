import pytest

from pymarc import Field, Record, Subfield

@pytest.fixture
def stub_title_no_number():
    return Field(
        tag="245",
        indicators=["1", "0"],
        subfields=[
            Subfield(code="a", value="Foo /"),
            Subfield(code="c", value="Spam.")
        ]
    )

@pytest.fixture
def stub_title_with_number():
    return Field(
        tag="245",
        indicators=["1", "0"],
        subfields=[
            Subfield(code="a", value="Foo :"),
            Subfield(code="b", value="bar."),
            Subfield(code="n", value="Book 3 /"),
            Subfield(code="c", value="by John Smith.")
        ]
    )