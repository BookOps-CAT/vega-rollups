import re
from typing import Optional

from pymarc import Field, Subfield


def add_custom_load_table_command(load_table: str) -> Field:
    if not load_table:
        raise ValueError("load_table argument cannot be empty.")

    return Field(
        tag="949",
        indicators=[" ", " "],
        subfields=[Subfield("a", f"*recs={load_table};")],
    )


def has_complex_subfields(field: Field) -> bool:
    for code in "dfghkmnoprs":
        if code in field:
            return True

    return False


def has_single_subfield_n(field: Field) -> bool:
    subs = field.get_subfields("n")
    if len(subs) == 1:
        return True
    else:
        return False


def normalize_value(value: str) -> str:
    return "".join(x for x in value if x.isalnum())


def complex_subfield_n(value: str) -> bool:
    match = re.match(r".*\d+\D+\d+|^\D+$", value)
    if match:
        return True
    else:
        return False


def find_digits(value: str) -> str:
    if complex_subfield_n(value):
        return None
    else:
        for c in value.split(" "):
            norm_c = normalize_value(c)
            if norm_c.isdigit():
                return norm_c


def get_number(field: Field) -> Optional[str]:
    """
    Returns a number from the first encountered subield $n
    """
    if field.tag != "245":
        raise ValueError("Invalid MARC tag passed. Only 245 is accepted.")

    if has_single_subfield_n(field):
        number = field["n"]
        number = find_digits(number)
        return number
    else:
        return None


def determine_subfield_n_position(field: Field) -> int:
    if "6" in field:
        return 2
    else:
        return 1


def modify_uniform_title(number: str, field: Field) -> Optional[Field]:
    """
    Inserts number into the subfield $n of 240 field
    """
    if not field:
        return None
    if field.tag != "240":
        raise ValueError("Invalid MARC tag passed. Only 240 is accepted.")

    if has_complex_subfields(field):
        return None
    elif not number:
        return None
    else:
        pos = determine_subfield_n_position(field)
        try:
            if field["l"][-1] == ".":
                field["l"] = field["l"][:-1]
        except KeyError:
            pass
        field.add_subfield("n", f"{number}.", pos)
        return field
