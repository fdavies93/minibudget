# MiniBudget

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

MiniBudget is a tool designed to enable personal and small business
budgeting using a plaintext format. It's inspired by [beancount](https://github.com/beancount/beancount) and [plainbudget](https://github.com/galvez/plainbudget).

I wrote the MVP in an evening because:

1. Beancount doesn't have a budgeting feature
2. Google Sheets seemed far too complex and inefficient for such a simple set of operations

## Quickstart

### Install with pipx

This is the recommended way to use minibudget. First [install pipx](https://pipx.pypa.io/stable/installation/) if you
don't already have it.

Then install. It's best to install the version with `[convert]` extras.

```sh
pipx install "minibudget[convert]" --pip-args "'--pre'"
```

You should be able to run `minibudget` from the command line like other CLI tools:

```sh
wget https://raw.githubusercontent.com/fdavies93/minibudget/refs/heads/main/budgets/example.budget
minibudget report example.budget
```

### Run from Source

Clone the repo. [Poetry](https://python-poetry.org/) is the easiest way to run it.

```sh
poetry run minibudget report budgets/example.budget
```

Now take a look at `example.budget` to learn more about it.

If you want to use the convert feature then use `poetry install -E convert` to 
get the required packages.

## Documentation

- [budget format](docs/budget-format.md) 
- [`minibudget report`](docs/report.md)
- [`minibudget diff`](docs/diff.md)
- [`minibudget convert`](docs/convert.md)
- [currency formats](docs/currency-formats.md)

## Possible Features

Since this is a deliberately simple tool, the preferred way to implement these 
is as command line options which generate different types of output. A proper 
TUI in curses or similar would make this into a finance tool from the 80s, 
which is probably redundant versus a web app.

**Pull requests welcome. I may or may not implement these myself when I feel 
like it.**

- [ ] Attach notes to budget categories; view them by using a flag
- [ ] Comment syntax
- [ ] Metadata for specifying period the budget covers, default currency, etc. 
- [ ] Assertions by allocating to categories with children; check if the budget for a category matches the total of its children (e.g. does discretionary spending match the totals of clothes, dining out, and entertainment?)
- [ ] Make formatting and report structure customizable
- [ ] Generate cool charts
- [ ] Proper multi-currency support (this is probably out of scope for a simple tool like this)
- [ ] Implement non-regression and unit testing
- [ ] CSV output options, especially for `diff` (as table grows large very quickly)
- [ ] JSON output options, mainly for testing but could be used for integrations
- [ ] Convert ledger records to minibudget format
- [ ] Convert csvs to minibudget format

## Completed Features

- [x] Cool formatting for CLI
- [x] Integrate with beancount via bean-query to import real spending
- [x] Totals for budget categories, not just the top level income / expenses / unassigned

