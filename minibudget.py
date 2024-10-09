#!python
from argparse import ArgumentParser
from copy import deepcopy
from model import Entry, EntryTreeNode, ReportData 
import render
from render import RenderData
import parse
import transform

def main():
    parser = ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--width", type=int, default=80)
    parser.add_argument("--currency-format", 
                        default="{neg}${amount}", 
                        help="Currency format, using Python format string syntax. E.g. {neg}${amount}")
    parser.add_argument("--currency-decimals", 
                        type=int, 
                        default=2, 
                        help="Number of decimal places to display when rendering currency. E.g. 2 will render as $0.00, while 0 will render as $0.")
    parsed = parser.parse_args()

    if parsed.width <= 0:
        raise ValueError("Display width must be more than 0.")

    if parsed.currency_decimals < 0:
        raise ValueError("Currency decimals must be 0 or more.")

    entries = parse.budget(parsed.file)
    
    render_data = RenderData(
        parsed.width,
        parsed.currency_format,
        parsed.currency_decimals
    )

    report_data = transform.entries_to_report_data(entries)

    render.report(report_data, render_data)


if __name__ == "__main__":
    main()
