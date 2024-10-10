from copy import deepcopy
import enum
from model import EntryTreeNode, ReportData
from dataclasses import dataclass
from enum import IntEnum

@dataclass
class RenderOptions:
    width: int
    currency_format: str
    currency_decimals: int

PREDEFINED_CURRENCIES = {
    "NTD": RenderOptions(width=0, currency_format="{neg}{amount} NTD", currency_decimals=0),
    "USD": RenderOptions(width=0, currency_format="{neg}${amount}", currency_decimals=2)
}


class Alignment(IntEnum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class Column:
    def __init__(self):
        self.cells = []
        self.align = Alignment.LEFT
        self.width = 0

    def add_cell(self, content: str):
        lines = content.split('\n')
        for line in lines:
            if text_len(line) > self.width:
                self.width = text_len(line)
        self.cells.append(content)

class Table:
    def __init__(self):
        self.columns: list[Column] = []

    def render(self, options: RenderOptions):
        table_width = sum([ col.width for col in self.columns ])
        # adjust for drawing column lines
        table_width += len(self.columns) + 1
        # adjust for padding
        table_width += len(self.columns) * 2
        
        table_rows = max( [len(col.cells) for col in self.columns] )

        output: list[str] = []
        # Iterate through rows; we'll break out of this later.
        row_i = 0
        while True:
            # Draw the top border of the table
            if row_i == 0:
                line = "┌"
                for j, col in enumerate(self.columns):
                    line += ("─" * (col.width + 2))
                    if j < len(self.columns) - 1:
                        line += "┬" 
                    else:
                        line += "┐"
                output.append(line)
            max_height = 1
            # since we want each row to be the right height
            for col in self.columns:
                lines = col.cells[row_i].split("\n")
                if len(lines) > max_height:
                    max_height = len(lines)
            # finally, we can render the (logical) row
            rows = ["" for _ in range(max_height)]
            footer = "├"
            for i, col in enumerate(self.columns):
                # We do this so we can render multi-line cells
                content_split = col.cells[row_i].split("\n")
                # Draw left table border 
                if i == 0:
                    for j, _ in enumerate(rows): 
                        rows[j] += "│ "
                # Actually render the cell contents
                for i2, _ in enumerate(rows):
                    if len(content_split) > i2:
                        rows[i2] += render_aligned(content_split[i2],col.width,col.align)
                    else:
                        rows[i2] += " " * col.width
                # Add column divider
                for j, _ in enumerate(rows): rows[j] += " │ "
            # Draw the footer for this row including + joins
            for j, col in enumerate(self.columns):
                footer += ("─" * (col.width + 2))
                if j < len(self.columns) - 1:
                    footer += "┼"
                else: footer += "┤"
            # We draw a different footer on the last row of the table
            if row_i != table_rows - 1:
                rows.append(footer)
            # Add *all* the lines of text to output, completing this logical row
            output.extend(rows)
            # Draw the bottom border of the table
            if row_i == table_rows - 1:
                line = "└"
                for j, col in enumerate(self.columns):
                    line += "─" * (col.width + 2)
                    if j < len(self.columns) - 1:
                        line += "┴"
                    else:
                        line += "┘"
                output.append(line)
                return output
            row_i += 1

# Get the text length of the string, not including
# console escape characters. Useful for making sure
# other formatting doesn't break (e.g. tables)
def text_len(text: str):
    new_text = deepcopy(text)
    for i in range(30):
        new_text = new_text.replace(f"\033[{i}m","")
    return len(new_text)

def render_right(text: str, width: int):
    padding = width - text_len(text)
    return (padding * " ") + text

def render_left(text: str, width: int):
    padding = width - text_len(text)
    return text + (padding * " ")

def render_center(text: str, width: int):
    padding: int = width - text_len(text)
    if padding % 2 == 1:
        left_pad = " " * int((padding - 1) / 2)
        right_pad = " " * int((padding + 1) / 2)
    else:
        left_pad = " " * int(padding / 2)
        right_pad = " " * int(padding / 2)
    
    return left_pad + text + right_pad

def render_aligned(text: str, width: int, aligned: Alignment):
    if aligned == Alignment.LEFT:
        return render_left(text, width)
    elif aligned == Alignment.RIGHT:
        return render_right(text, width)
    elif aligned == Alignment.CENTER:
        return render_center(text, width)

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
