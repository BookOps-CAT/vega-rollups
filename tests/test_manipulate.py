import pytest


from manipulate import keep_fields


def test_keep_fields(stub_bib):
    # make sure the following tags are present in the stub
    assert "020" in stub_bib
    assert "100" in stub_bib
    assert "264" in stub_bib
    assert "300" in stub_bib

    keep_fields(stub_bib, ["008", "240", "245"])
    assert len(stub_bib.fields) == 3
    assert "008" in stub_bib
    assert "240" in stub_bib
    assert "245" in stub_bib
