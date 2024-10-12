from dataclasses import dataclass
from typing import Union

@dataclass
class Entry:
    categories: list[str]
    is_income: bool
    is_calculated: bool
    amount: int
    children: list[str]
 
@dataclass
class ReportData:
    entries: list[Entry]
    total_income: int
    income_dict: dict[str, Entry]
    total_expenses: int
    expense_dict: dict[str, Entry]
    total_unassigned: int

@dataclass 
class DiffTreeNode:
    category_name: str
    category_totals: list[int] 
    children: dict[str, "DiffTreeNode"]
