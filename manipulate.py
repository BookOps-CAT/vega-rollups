import csv, sys

from pymarc import MARCReader, Record

from copy_number import get_number, modify_uniform_title


def save2csv(dst_fh, row):
    """
    Appends a list with data to a dst_fh csv
    args:
        dst_fh: str, output file
        row: list, list of values to write in a row
    """

    with open(dst_fh, "a", encoding="utf-8") as csvfile:
        out = csv.writer(
            csvfile,
            delimiter=",",
            lineterminator="\n",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        try:
            out.writerow(row)
        except UnicodeEncodeError:
            pass


def save2marc(dst: str, record: Record) -> None:
    with open(dst, "ab") as marcfile:
        marcfile.write(record.as_marc())


def process(src: str, dst: str):
    with open(src, "rb") as marcfile:
        reader = MARCReader(marcfile, hide_utf8_warnings=True)
        for record in reader:
            bibNo = record["907"]["a"][1:].strip()
            t245 = record["245"]
            number = get_number(t245)
            t240 = record["240"]
            new_t240 = modify_uniform_title(number, t240)
            if new_t240:
                record.remove_field(t240)
                record.add_ordered_field(new_t240)
                save2marc(dst, record)
                save2csv("processed.csv", [bibNo, str(t245), str(new_t240)])
            else:
                save2csv("skipped.csv", [bibNo, str(t245)])


if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]

    process(src, dst)
