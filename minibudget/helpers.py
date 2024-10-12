from collections.abc import Callable
from typing import Union
from minibudget.model import Entry

def _dft_entry_dict(entry_dict: dict[str, Entry], root: str, fn: Union[None, Callable]):
    root_entry = entry_dict[root]
    if fn != None:
        fn(root_entry)
    for child in root_entry.children:
        _dft_entry_dict(entry_dict, child, fn)
        
def dft_entry_dict(entry_dict: dict[str, Entry], fn: Union[None, Callable] = None):
    roots = [ key for key in entry_dict.keys() if len(key.split(":")) == 1 ]
    for root in roots:
        _dft_entry_dict( entry_dict, root, fn )

def _dft_diff_dict(entry_dict: dict[str, list[Union[Entry, None]]], root: str, fn: Union[None, Callable]):
    root_list = entry_dict[root]
    if fn != None:
        fn(root_list)
    children = set()
    for entry in root_list:
        if entry == None:
            continue
        children.update(entry.children)
    for child in children:
        _dft_diff_dict(entry_dict, child, fn)

def dft_diff_dict(entry_dict: dict[str, list[Union[Entry, None]]], fn: Union[None, Callable]):
    roots = [ key for key in entry_dict.keys() if len(key.split(":")) == 1 ]
    for root in roots:
        _dft_diff_dict( entry_dict, root, fn )
