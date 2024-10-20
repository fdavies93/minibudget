#!python
from argparse import ArgumentParser
from minibudget.parsers import ReportParser, DiffParser, ConvertParser

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    ReportParser.setup(subparsers)
    DiffParser.setup(subparsers)
    ConvertParser.setup(subparsers)

    args = parser.parse_args()
    args.func(args) 

if __name__ == "__main__":
    main()
