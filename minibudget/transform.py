from typing import Union
from minibudget.model import Entry, ReportData, DiffTreeNode
from copy import deepcopy

def calculate_total(entries: list[Entry]) -> int:
    total = 0

    for entry in entries:        
        to_add = entry.amount
        
        total += to_add

    return total

# By generating categories this way we can render as a tree
# without the algorithmic complexity of storing the information
# as a tree; instead we're using a method similar to a DAG
# representation in the dictionary.
def generate_category_dict(entries: list[Entry]) -> dict[str, Entry]:
    base_output: dict[str, Entry] = {}
    for entry in entries:
        key = ":".join(entry.categories)
        base_output[key] = entry
   
    output = deepcopy(base_output) 
    for entry_key, entry in base_output.items():
        categories = entry_key.split(":")
        last_category = entry_key
        for i in range(1, len(categories)):
            parent_categories = categories[:-i]
            category_key = ":".join(parent_categories)
            if category_key in output:
                output[category_key].amount += entry.amount
                if last_category not in output[category_key].children:
                    output[category_key].children.append(last_category)
                last_category = category_key
                continue
            output[category_key] = Entry(parent_categories,
                                         entry.is_income,
                                         True, 
                                         entry.amount,
                                         [last_category]
                                         )
            last_category = category_key
    return output

def generate_diff_dict(category_dicts: list[dict[str, Entry]]) -> dict[str, list[Union[Entry, None]]]:
    diff_dict = {}
    for dict_i, category_dict in enumerate(category_dicts): 
        for key, entry in category_dict.items():
            if key not in diff_dict:
                diff_dict[key] = [None] * len(category_dicts)
            diff_dict[key][dict_i] = entry
    return diff_dict

def entries_to_report_data(entries: list[Entry]) -> ReportData:
    income_entries = list(filter(lambda e: e.is_income, entries))
    expense_entries = list(filter(lambda e: not e.is_income, entries))
    
    report_data = ReportData(
        entries,
        calculate_total(income_entries),
        generate_category_dict(income_entries),
        calculate_total(expense_entries),
        generate_category_dict(expense_entries),
        calculate_total(entries)
    )
    return report_data
