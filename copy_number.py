from typing import Optional

from pymarc import Field


def has_complex_subfields(field: Field) -> bool:
    for code in "dfghkmnoprs":
        if code in field:
            return True

    return False


def normalize_value(value: str) -> str:
    return "".join(x for x in value if x.isalnum())


def find_digits(value: str) -> str:
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

    try:
        number = field["n"]
        number = find_digits(number)
        return number
    except KeyError:
        return None


def modify_uniform_title(number: str, field: Field) -> Field:
    """
    Inserts number into the subfield $n of 240 field
    """
    if field.tag != "240":
        raise ValueError("Invalid MARC tag passed. Only 240 is accepted.")

    if has_complex_subfields(field):
        return None
    elif not number:
        return None
    else:
        field.add_subfield("n", f"{number}.", 1)
        return field
