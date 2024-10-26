import rich
from rich.markup import render
from minibudget.model import ReportData, Entry
from dataclasses import dataclass
from minibudget.helpers import dft_diff_dict, dft_entry_dict
from rich.table import Table
from rich.text import Text
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

def report_table(title: str,categories: dict[str, Entry], total: int, render_data: RenderOptions) -> Table: 
    table = Table(title=title, expand=True)
    if render_data.width != None:
        table.width = render_data.width
        table.expand = False
    table.add_column("Category", ratio=5)
    table.add_column("Amount", justify="right", ratio=2)

    def render_category(entry: Entry):
        depth = len(entry.categories) - 1
        tag = entry.categories[-1]
        left = f"{" " * 4 * depth}{tag}"
        right = currency(entry.amount, render_data)
        table.add_row(left, right)
    
    dft_entry_dict(categories, fn=render_category)
    table.add_section()
    table.add_row("Total", currency(total, render_data))

    return table

def diff_tree(tree: dict[str, list[Union[Entry, None]]], names: list[str], render_data: RenderOptions) -> Table:
    table = Table(expand=True)
    if render_data.width != None:
        table.width = render_data.width
        table.expand = False
    table.add_column("Category")
    for name in names:
        table.add_column(name, justify="right")
 
    def render_category(entries: list[Union[Entry, None]]):
        amounts = []
        for entry in entries:
            if entry == None:
                amounts.append(0)
            else:
                amounts.append(entry.amount)
        tag = ""
        depth = 0 

        for entry in entries:
            if entry != None:
                tag = entry.categories[-1]
                depth = len(entry.categories) - 1

        category = f"{"    "*depth}{tag}"
        cells = [Text( currency(amounts[0], render_data) )]

        for i, amount in enumerate(amounts[1:]):
            diff = amount - amounts[i]
            amount_rendered = f"{currency(amount, render_data)}\n"
            diff_rendered = Text(currency(diff, render_data))
            if diff > 0:
                diff_rendered.stylize("green")
            elif diff == 0:
                diff_rendered.stylize("dim")
            elif diff < 0:
                diff_rendered.stylize("red")
            cells.append( Text.assemble(amount_rendered,diff_rendered) )
        
        if depth == 0:
            table.add_section()
        table.add_row( category, *cells )
        if depth == 0:
            table.add_section()
        
    dft_diff_dict(tree, fn=render_category)
    return table


def diff_csv(
        tree: dict[str, list[Union[Entry, None]]],
        names: list[str],
        render_data: RenderOptions
) -> list[list[str]]: 
    rows = []
    header = ["Category"] + names

    # add diff column headers
    for i, name in enumerate(names[1:]):
        header.append(f"diff({names[i]},{name})")

    rows.append(header)
 
    def render_category(entries: list[Union[Entry, None]]):
        amounts = []
        for entry in entries:
            if entry == None:
                amounts.append(0)
            else:
                amounts.append(entry.amount)

        tag = ""
        for entry in entries:
            if entry != None:
                tag = ":".join(entry.categories)
        
        row = [tag]
        # add raw amounts
        for amount in amounts:
            row.append(currency(amount, render_data)) 
        # add diff columns
        for i, amount in enumerate(amounts[1:]):
            diff = amount - amounts[i]
            row.append(currency(diff, render_data))
 
        rows.append(row)

    dft_diff_dict(tree, fn=render_category)

    return rows

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

def report(data: ReportData, render_data: RenderOptions):
    console = rich.console.Console()
    
    income_table = report_table("Income",data.income_dict, data.total_income, render_data)
    expense_table = report_table("Expenses",data.expense_dict, data.total_expenses, render_data)

    unassigned_style = "default"
    unassigned_string = "All funds have been assigned. =)"

    if data.total_unassigned < 0:
        unassigned_style = "red"
        unassigned_string = currency(data.total_unassigned, render_data)
    elif data.total_unassigned > 0:
        unassigned_style = "green"
        unassigned_string = currency(data.total_unassigned, render_data)

    unassigned_table = Table(expand=True, show_header=False, border_style=unassigned_style, row_styles=[unassigned_style])
    
    if render_data.width != None:
        unassigned_table.width = render_data.width
        unassigned_table.expand = False

    unassigned_table.add_column(ratio=5)
    unassigned_table.add_column(justify="right", ratio=2)

    unassigned_table.add_row("Unassigned funds", unassigned_string)
 
    console.print(income_table, expense_table, unassigned_table)
 
def diff(reports: list[ReportData], render_data: RenderOptions):
    pass
