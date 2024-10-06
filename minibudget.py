from argparse import ArgumentParser
from dataclasses import dataclass
import sys
from copy import deepcopy
from typing import Union

@dataclass
class Entry:
    categories: list[str]
    is_expense: bool
    amount: int
    currency: str

@dataclass
class EntryTreeNode:
    entry: Union[Entry,None]
    children: dict[str, "EntryTreeNode"]

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

def generate_category_tree(entries: list[Entry]) -> EntryTreeNode:
    root = EntryTreeNode(None, {}) 
    for entry in entries:
        cur = root
        categories = deepcopy(entry.categories)
        while len(categories) > 0:
            next = categories[0]
            categories.remove(next)
            if next not in cur.children:
                cur.children[next] = EntryTreeNode(None, {}) 
            cur = cur.children[next]
        if cur.entry is not None:
            raise ValueError("Cannot have two categories with identical names!")
        cur.entry = entry
    return root

def format_category_tree(tree: EntryTreeNode, width=80, depth=0) -> list[str]:
    lines = []
    for tag, child in tree.children.items():
        left = f"{"    "*depth}{tag}"
        right = ""
        if child.entry is not None:
            right = f"{child.entry.amount} {child.entry.currency}"
        spacer = " " * (width - (len(left) + len(right)))
        lines.append(f"{left}{spacer}{right}")
        lines.extend(format_category_tree(child, 80, depth+1))
    return lines

def generate_total_header(heading: str, total: int, currency: str, width=80) -> list[str]:
    lines = ["-" * width] 
   
    right = f"{total} {currency}"
    spacer = " " * ( width - (len(heading) + len(right)) )
    lines.append(f"{heading}{spacer}{right}")
    lines.append("-" * width)
    return lines

def generate_income_report(entries: list[Entry], width=80):
    income_entries = list(filter(lambda e: not e.is_expense, entries))
    total = sum([e.amount for e in income_entries])
    tree = generate_category_tree(income_entries)
    output = generate_total_header("INCOME", total, income_entries[0].currency, width)
    output.extend(format_category_tree(tree, width))
    return "\n".join(output)
    
def generate_expense_report(entries: list[Entry], width=80):
    expense_entries = list(filter(lambda e: e.is_expense, entries))
    total = sum([e.amount for e in expense_entries])
    tree = generate_category_tree(expense_entries)
    output = generate_total_header("EXPENSES", total, expense_entries[0].currency, width)
    output.extend(format_category_tree(tree, width))
    return "\n".join(output)

def report_budget(entries: list[Entry]):
    totals = calculate_totals(entries)
     
    print(generate_income_report(entries))
    print(generate_expense_report(entries))

    total_head = entries[0].currency
    print(
        "\n".join(generate_total_header("UNASSIGNED",totals[total_head],total_head, 80))
    )

def main():
    parser = ArgumentParser()
    parser.add_argument("file")
    parsed = parser.parse_args()

    entries = parse_budget(parsed.file)
    report_budget(entries)

if __name__ == "__main__":
    main()
