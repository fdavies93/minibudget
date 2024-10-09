from model import Entry, EntryTreeNode, ReportData
from copy import deepcopy

def calculate_total(entries: list[Entry]) -> int:
    total = 0

    for entry in entries:        
        to_add = entry.amount
        if entry.is_expense:
            to_add *= -1

        total += to_add

    return total

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

def entries_to_report_data(entries: list[Entry]) -> ReportData:
    income_entries = list(filter(lambda e: not e.is_expense, entries))
    expense_entries = list(filter(lambda e: e.is_expense, entries))
    income_tree = generate_category_tree(income_entries)
    expenses_tree = generate_category_tree(expense_entries)

    report_data = ReportData(
        entries,
        income_tree,
        expenses_tree,
        calculate_total(income_entries),
        calculate_total(expense_entries),
        calculate_total(entries)
    )
    return report_data
