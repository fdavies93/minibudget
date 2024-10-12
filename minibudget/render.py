from minibudget.model import ReportData, Entry
from dataclasses import dataclass
from minibudget.helpers import dft_diff_dict, dft_entry_dict
import rich
from typing import Union

@dataclass
class RenderOptions:
    width: int
    currency_format: str
    currency_decimals: int

PREDEFINED_CURRENCIES = {
    "NTD": RenderOptions(width=0, currency_format="{neg}{amount} NTD", currency_decimals=0),
    "USD": RenderOptions(width=0, currency_format="{neg}${amount}", currency_decimals=2)
}

def category_tree(categories: dict[str, Entry], render_data: RenderOptions) -> list[str]:
    width = render_data.width
    lines = []
    
    def render_category(entry: Entry):
        depth = len(entry.categories) - 1
        tag = entry.categories[-1]
        left = f"{"    "*depth}{tag}"
        right = currency(entry.amount, render_data)
        spacer = " " * (width - (len(left) + len(right)))
        lines.append(f"{left}{spacer}{right}")

    dft_entry_dict(categories, fn=render_category )
    return lines

def diff_tree(tree: dict[str, list[Union[Entry | None]]], render_data: RenderOptions) -> list[str]:
    lines = []

    def render_category(entries: list[Entry]):
        amounts = [ str(entry.amount) for entry in entries ]
        tag = ""
        depth = 0 

        for entry in entries:
            if entry != None:
                tag = entry.categories[-1]
                depth = len(entry.categories) - 1

        left = f"{"    "*depth}{tag}"
        right = ", ".join(amounts)
        lines.append(f"{left} | {right}")

    dft_diff_dict(tree, fn=render_category)
    return lines

def currency(units: int, render_data: RenderOptions) -> str:
    # so we can do e.g. -$100 instead of $-100
    amount = str(abs(units))
    decimal = render_data.currency_decimals
    if decimal > 0:
        left = amount[:-decimal]
        if len(left) == 0:
            left = "0"
        right = amount[-decimal:]
        while len(right) < decimal:
            right += "0"
        amount = left + "." + right
    output = render_data.currency_format.format(amount=amount, neg="-" if units < 0 else "") 
    return output

def total_header(heading: str, total: int, render_data: RenderOptions) -> list[str]:
    width = render_data.width
    lines = ["-" * width]
    right = currency(total, render_data)
    spacer = " " * ( width - (len(heading) + len(right)) )
    lines.append(f"{heading}{spacer}{right}")
    lines.append("-" * width)
    return lines

def report(data: ReportData, render_data: RenderOptions):
    lines = [
        *total_header("INCOME", data.total_income,render_data),
        *category_tree(data.income_dict, render_data),
        *total_header("EXPENSES", data.total_expenses,render_data),
        *category_tree(data.expense_dict, render_data),
        *total_header("UNASSIGNED", data.total_unassigned,render_data)
    ]
    print("\n".join(lines))

def diff(reports: list[ReportData], render_data: RenderOptions):
    pass
