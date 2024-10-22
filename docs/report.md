# `minibudget report`

`minibudget report` is the basic view of minibudget. It shows a summary of income
and expenses in the budget, with the total unallocated income at the bottom.

You can try to keep the unallocated budget green and use this as a savings
indicator, or you can allocate savings as an expenses category as in
[the envelope budgeting method](https://www.investopedia.com/envelope-budgeting-system-5208026).

## Basic Usage

The report command takes one argument: the filename of a budget file.

```sh
minibudget report ./example.budget 
```

This will create a chart of accounts for income and expenses based on the input
file.

## Options

### Rendering

`--width`

The width of the output report, in characters. Defaults to the full screen width.

`--currency-format`

The currency format as a Python format string. For example, for USD:

`{neg}${amount}`

When combined with `--currency decimals` for -500 units this will output `-$5.00`.

`--currency-decimals`

This is the number of decimal points to render the currency with. For example
USD has 2 and 1000 units will be rendered as `10.00`, while NTD has 0 and
1000 units will be rendered as `1000`.

`--currency`

This is a shortcut for `--currency-format` and `--currency-decimals`. Defaults to USD.

Currently we support these [built-in currency formats](currency-formats.md)
