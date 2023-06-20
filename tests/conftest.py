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


@pytest.fixture
def stub_bib(stub_240, stub_245_with_number):
    bib = Record()
    bib.leader = "00000nam a2200000u  4500"
    bib.add_field(Field(tag="008", data="20230616s        xx            000 u eng d"))
    bib.add_field(
        Field(tag="020", indicators=[" ", " "], subfields=[Subfield("a", "1234")])
    )
    bib.add_field(
        Field(
            tag="100", indicators=["1", "0"], subfields=[Subfield("a", "Smith, John.")]
        )
    )
    bib.add_field(stub_240)
    bib.add_field(stub_245_with_number)
    bib.add_field(
        Field(
            tag="264",
            indicators=[" ", "1"],
            subfields=[
                Subfield("a", "New York:"),
                Subfield("b", "Orion,"),
                Subfield("c", "2023."),
            ],
        )
    )
    bib.add_field(
        Field(
            tag="300",
            indicators=[" ", " "],
            subfields=[Subfield("a", "250 pages;"), Subfield("c", "23 cm")],
        )
    )
    return bib
