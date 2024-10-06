from argparse import ArgumentParser
from dataclasses import dataclass
import sys

@dataclass
class Entry:
    categories: list[str]
    is_expense: bool
    amount: int
    currency: str

def tokenise_line(line: str) -> list[str]:
    delimiter = "\""
    separator = " \n"
    buffer = ""
    fields = []
    delimited = False
    for char in line:
        if char == delimiter:
            delimited = not delimited
        elif char in separator and not delimited and len(buffer) > 0:
            fields.append(buffer)
            buffer = ""
        elif (char not in separator) or delimited:
            buffer += char
    return fields

def parse_line(line: str) -> Entry:
    fields = tokenise_line(line)
    
    if fields[0] not in "+-":
        raise ValueError("Only + and - are valid entries for a start of line.")

    is_expense = fields[0] == "-"

    categories = fields[1].split(":")
    amount = int(fields[2])
    currency = fields[3]

    return Entry(
        categories=categories,
        is_expense=is_expense,
        amount=amount,
        currency=currency
    )

def parse_budget(filename: str):
    entries: list[Entry] = []
    with open(filename) as f:
        for i, line in enumerate(f):
            try:
                entry = parse_line(line)
                entries.append(entry)
            except Exception as err:
                print(err,file=sys.stderr)
                print(f"Couldn't parse line {i}; {line}.", file=sys.stderr) 
    return entries

def calculate_totals(entries: list[Entry]):
    totals = {}

    for entry in entries:
        if entry.currency not in totals:
            totals[entry.currency] = 0
        
        to_add = entry.amount
        if entry.is_expense:
            to_add *= -1

        totals[entry.currency] += to_add

    return totals

def generate_income_report(entries: list[Entry]):
    lines = []

    for entry in entries:
        category_tag = "/".join(entry.categories)
        amount_part = f"{entry.amount} {entry.currency}"
        spacer = (80-(len(category_tag) + len(amount_part)))*" "
        if not entry.is_expense:
            lines.append(f"{category_tag}{spacer}{amount_part}")
    return "\n".join(lines)

def generate_expense_report(entries: list[Entry]):
    lines = []
    for entry in entries:
        category_tag = "/".join(entry.categories)
        amount_part = f"{entry.amount} {entry.currency}"
        spacer = (80-(len(category_tag) + len(amount_part)))*" "
        if entry.is_expense:
            lines.append(f"{category_tag}{spacer}{amount_part}")
    return "\n".join(lines)


def report_budget(entries: list[Entry]):
    totals = calculate_totals(entries)
    
    separator = "-"*80

    print(separator)
    print("INCOME")
    print(separator)
    print(generate_income_report(entries))
    print(separator)
    print("EXPENSES")
    print(separator)
    print(generate_expense_report(entries))
    print(separator)
    print("UNASSIGNED")
    print(separator)
    for key, value in totals.items():
        print(f"{value} {key}")
    print(separator)

def main():
    parser = ArgumentParser()
    parser.add_argument("file")
    parsed = parser.parse_args()

    entries = parse_budget(parsed.file)
    report_budget(entries)

if __name__ == "__main__":
    main()
