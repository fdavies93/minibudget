from minibudget.model import Entry
import sys

def tokenise_line(ln: str) -> list[str]:
    delimiter = "\""
    separator = " \n"
    buffer = ""
    fields = []
    delimited = False
    for char in ln:
        if char == delimiter:
            delimited = not delimited
        elif char in separator and not delimited and len(buffer) > 0:
            fields.append(buffer)
            buffer = ""
        elif (char not in separator) or delimited:
            buffer += char
    return fields

def line(ln: str) -> Entry:
    fields = tokenise_line(ln)
    
    if fields[0] not in "+-":
        raise ValueError("Only + and - are valid entries for a start of line.")

    is_expense = fields[0] == "-"

    categories = fields[1].split(":")
    amount = int(fields[2])

    if is_expense:
        amount = amount * -1

    return Entry(
        categories=categories,
        is_income=not is_expense,
        is_calculated=False,
        amount=amount,
        children=[]
    )

def budget(filename: str):
    entries: list[Entry] = []
    with open(filename) as f:
        for i, ln in enumerate(f):
            try:
                entry = line(ln)
                entries.append(entry)
            except Exception as err:
                print(err,file=sys.stderr)
                print(f"Couldn't parse line {i}; {ln}.", file=sys.stderr) 
    return entries

