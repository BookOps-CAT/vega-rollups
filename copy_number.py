from typing import Optional

from pymarc import Field


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
