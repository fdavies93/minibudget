# MiniBudget

MiniBudget is a tool designed to enable personal and small business
budgeting using a plaintext format. It's inspired by [beancount](https://github.com/beancount/beancount) and [plainbudget](https://github.com/galvez/plainbudget).

I wrote the MVP in an evening because:

1. Beancount doesn't have a budgeting feature
2. Google Sheets seemed far too complex and inefficient for such a simple set of operations

## Get Started

Clone the repo.

```sh
python minibudget.py example.budget
```

Now take a look at `example.budget` to learn more about it.

## Possible Features

Since this is a deliberately simple tool, the preferred way to implement these is as command line options which generate different types of output. A proper TUI in curses or similar would make this into a finance tool from the 80s, which is probably redundant versus a web app.

**Pull requests welcome. I may or may not implement these myself when I feel like it.**

- [ ] Attach notes to budget categories; view them by using a flag
- [ ] Metadata for specifying period the budget covers, default currency, etc. 
- [ ] Integrate with beancount via bean-query to import real spending
- [ ] Compare real spending to budgeted spending over a period
- [ ] Totals for budget categories, not just the top level income / expenses / unassigned
    - [ ] Assertions by allocating to categories with children; check if the budget for a category matches the total of its children (e.g. does discretionary spending match the totals of clothes, dining out, and entertainment?)
- [ ] Cool formatting for CLI
    - [ ] Make formatting and report structure customizable
- [ ] Generate cool charts
- [ ] Proper multi-currency support (this is probably out of scope for a simple tool like this)
