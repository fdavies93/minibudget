from model import EntryTreeNode, ReportData
from dataclasses import dataclass
import rich

@dataclass
class RenderOptions:
    width: int
    currency_format: str
    currency_decimals: int

PREDEFINED_CURRENCIES = {
    "NTD": RenderOptions(width=0, currency_format="{neg}{amount} NTD", currency_decimals=0),
    "USD": RenderOptions(width=0, currency_format="{neg}${amount}", currency_decimals=2)
}

def category_tree(tree: EntryTreeNode, render_data: RenderOptions, depth=0) -> list[str]:
    width = render_data.width
    lines = []
    for tag, child in tree.children.items():
        left = f"{"    "*depth}{tag}"
        amount = child.category_total
        right = currency(amount, render_data)
        right_width = len(right)
        if child.entry is None:
            right = f"{right}"
        spacer = " " * (width - (len(left) + right_width))
        lines.append(f"{left}{spacer}{right}")
        lines.extend(category_tree(child, render_data, depth+1))
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
        *category_tree(data.income_tree, render_data),
        *total_header("EXPENSES", data.total_expenses,render_data),
        *category_tree(data.expenses_tree, render_data),
        *total_header("UNASSIGNED", data.total_unassigned,render_data)
    ]
    print("\n".join(lines))
