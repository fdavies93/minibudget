#!python
from argparse import ArgumentParser
from minibudget.parsers import ReportParser, DiffParser, ConvertParser, ChartParser

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    to_use = (
        ReportParser,
        DiffParser,
        ConvertParser,
        ChartParser
    )
    
    for p in to_use:
        p.setup(subparsers)
    
    args = parser.parse_args()
    args.func(args) 

if __name__ == "__main__":
    main()
