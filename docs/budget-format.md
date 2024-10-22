# Minibudget Budget Format

The minibudget format is based on [plainbudget](https://github.com/galvez/plainbudget)
syntax and aims to be quick to write but powerful enough to produce useful
financial reports.

The file extension for minibudget is `.budget`

## Example

*example.budget*

```
+ Salary                 280000
- Essential:Rent         120000
- Essential:Food          30000
- "Debt:Tax"               5000
- "True Expenses:Home"    15000
- Savings                100000
```

## Format

One line of the report is 3 fields, which can be separated by any amount of 
whitespace. This lets you format the budget such that the numbers have a more
pleasing alignment. Leading and trailing whitespace is ignored. Everything after 
the 3rd field is also ignored.

These fields are as follows:

**Sign:** `+` or `-`. This is used to designate the number as income or expenses,
i.e. a `+ Foo 1000` entry is always classed as `Income:Foo`.

**Account:** An arbitrary string. This can be delimited by using `"Quote Marks"`
so that names are easier to read.

**Units:** Units of whichever currency the budget is in. This is normally the
smallest possible denomination (e.g. 100 units of USD is $1). For cryptocurrency
you may want to decide on a cutoff before making the budget: e.g. 1 unit of bitcoin
could represent 0.0000001 bitcoin to deal with its unusually high value. `report`
and `diff` can both use currency options to change how this is displayed. 
