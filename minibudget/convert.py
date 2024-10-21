import shutil
import subprocess
import csv
import io
from typing import Union
from minibudget.model import Entry
from decimal import Decimal

def beancount_to_entry(record: dict, currency: str) -> Union[Entry, None]:
    amount = 0
    found_currency = False
    for key, val in record.items():
        if len(val) == 0: continue
        if currency in key: 
            # since it's double-entry
            # income and expenses are reversed
            amount = Decimal(val) * -1
            found_currency = True
            break
    if not found_currency:
        return None
    categories = record["account"].split(":")
    return Entry(
        categories=categories[1:],
        is_calculated=False,
        is_income=(categories[0] == "Income"),
        # the linter hates this, but it's succinct
        amount = int(amount * (Decimal('10') ** -amount.as_tuple()[2])),
        children=[]
    )

def beancount(file: str, currency: str, start: str, end: str) -> list[Entry]:
    # Validate bean-query is in PATH
    if shutil.which("bean-query") == None:
        raise EnvironmentError("bean-query could not be found. Please make sure it's installed in your environment and try again.")
    date_part = ""
    date_inner = []
    if start != None:
        date_inner.append(f"date >= {start}")
    if end != None:
        date_inner.append(f"date <= {end}")
    if start != None or end != None:
        date_part = f" and ( { " and ".join(date_inner) } )"
    # Issue query to get chart of accounts
    output = subprocess.run(["bean-query",
                             file,
                             f"select account, sum(position) where (account ~ 'Expenses' or account ~ 'Income' ) {date_part} group by account order by account",
                             "--format",
                             "csv",
                             "-m"], 
                            capture_output=True)
    output_as_csv = csv.DictReader(io.StringIO(output.stdout.decode('utf-8')))
    # Filter chart of accounts to the currency we care about
    entries = []
    for record in output_as_csv:
        entry = beancount_to_entry(record, currency)
        if entry is None: continue
        entries.append(entry)
    # Return accounts in minibudget format
    return entries

def entry_list_to_string(entry_list: list[Entry], width = 80):
    str_list = []
    for entry in entry_list:
        left = ""
        right = ""
        if entry.is_income:
            left += "+ "
        else:
            left += "- "
        left += ":".join(entry.categories)
        right += str(abs(entry.amount))
        spacer = " " * (width - (len(left) + len(right)))
        str_list.append(f"{left}{spacer}{right}")
    return "\n".join(str_list)
