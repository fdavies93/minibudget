# `minibudget convert`

`minibudget convert` takes some other format and turns it into a minibudget
format. It's intended for taking real records of spending and converting them
so they can be used with `minibudget diff`.

Because of the additional tools needed to extract data from other formats
effectively, you'll need to install the extras package `convert` to use this
command.

## Basic Usage

`minibudget convert 2024-10.beancount > 2024-10.budget`

By default minibudget will try to infer the type of the imported file but you
can use the `--format` option to set this explicitly.

Minibudget outputs to stdout by default, so you'll need to pipe the output
into your desired `.budget` file.

## Options

`--width`

The width of the output budget in characters. Default is 80.

`--start`

The date to start calculating the budget from (inclusive) in ISO date format:
`2024-10-01`.

`--end`

The date to calculate the budget until (inclusive) in ISO date format:
`2024-10-31`.

`--currency`

The currency to convert into minibudget format, where multiple are available.
Minibudget only deals with a single currency per budget, so we need to choose 
one.

`--format`

Set the format of the input file explicitly.

## Supported Formats

### [Beancount](https://github.com/beancount/beancount)

Income and expenses accounts in Beancount are converted to `+` and `-` entries
in minibudget.

Since Beancount is double-entry accounting software, income is expressed as a
negative while expenses are positive. Minibudget reverses these so that they're
more intuitive in a traditional budget format.

Some types of expenses are not imported automatically: for example paying down
a credit card, where the credit card is recorded as a Liability, will not be
imported. You may need to add these manually.

And of course, if your accounts in Beancount are named differently to your 
budget categories in `minibudget`, you'll need to rename them in the `.budget`
file.
