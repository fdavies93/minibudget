from dataclasses import dataclass
from typing import Union

@dataclass
class Entry:
    categories: list[str]
    is_expense: bool
    amount: int
 
@dataclass
class EntryTreeNode:
    entry: Union[Entry,None]
    children: dict[str, "EntryTreeNode"]
    category_total: int = 0

@dataclass
class ReportData:
    entry_list: list[Entry]
    income_tree: EntryTreeNode
    expenses_tree: EntryTreeNode
    total_income: int
    total_expenses: int
    total_unassigned: int
