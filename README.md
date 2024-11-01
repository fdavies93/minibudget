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
- [`minibudget chart`](docs/chart.md)
- [currency formats](docs/currency-formats.md)

## Possible Features

Since this is a deliberately simple tool, the preferred way to implement these 
is as command line options which generate different types of output. A proper 
TUI in curses or similar would make this into a finance tool from the 80s, 
which is probably redundant versus a web app.

**Pull requests welcome. I may or may not implement these myself when I feel 
like it.**

### Budget Format / Parsing

- [ ] Attach notes to budget categories; view them by using a flag
- [ ] Comment syntax
- [ ] Metadata for specifying period the budget covers, default currency, etc. 
- [ ] Budget assertions for explicit and implicit categories
- [ ] Allow negative income and positive expenses accounts for edge cases
      in business & financial records.
- [ ] Add a formatting mode.
- [ ] Write a treesitter grammar for neovim etc.

### Data Handling

- [ ] Make treatment of numbers / currency consistent
    - [ ] Use Decimal / bespoke money handler consistently for currency
    - [ ] Write consistent currency formatter class or interface; build
          in concept of 'normal' decimalisation (e.g. USD has 2, NTD has 0).
- [ ] Proper multi-currency support
- [ ] Add more canned currency formats
- [ ] Implement non-regression and unit testing

### Conversion from other formats

- [ ] Convert ledger records to minibudget format
- [ ] Convert csvs to minibudget format
- [ ] Convert JSON output format back into 

### Outputs / rendering

- [ ] CSV output for `report`
- [ ] JSON output for `diff`
- [ ] JSON output for `report`
- [ ] Make formatting and report structure customizable
- [ ] Stacked bar chart for income and expenses over time (visualising `diff`)
- [ ] Sunburst chart for income reports, for people with many income streams

## Completed Features

- [x] Switch to Calendar Versioning (likely YYYY-MM-R or YYYY-MM-DD)
- [x] Sunburst chart for expenses reports
- [x] CSV output for `diff`
- [x] Cool formatting for CLI
- [x] Integrate with beancount via bean-query to import real spending
- [x] Totals for budget categories, not just the top level income / expenses / unassigned

