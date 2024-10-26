import csv
import sys
from minibudget import parse
from minibudget import render
from minibudget import transform
from minibudget import convert
from minibudget.render import RenderOptions
from rich.console import Console
from pathlib import Path

class CommonParser:
    @staticmethod
    def setup_render_options(parser):
        parser.add_argument("--width", help="Width of the rendered report in characters. Defaults to the space available in the terminal.", type=int)
        parser.add_argument("--currency", 
                            type=str, 
                            help="The currency to render this budget with. A shortcut for --currency-format and --currency-decimals")
        parser.add_argument("--currency-format", 
                            default="{neg}${amount}", 
                            help="Currency format, using Python format string syntax. E.g. {neg}${amount}")
        parser.add_argument("--currency-decimals", 
                            type=int, 
                            default=2, 
                            help="Number of decimal places to display when rendering currency. E.g. 2 will render as $0.00, while 0 will render as $0.")
    
    @staticmethod
    def get_render_options(args) -> RenderOptions: 
        if args.currency_decimals < 0:
            raise ValueError("Currency decimals must be 0 or more.")
        
        render_data = RenderOptions(
                    args.width,
                    args.currency_format,
                    args.currency_decimals
                )

        if args.currency in render.PREDEFINED_CURRENCIES:
            currency_data = render.PREDEFINED_CURRENCIES[args.currency]
            render_data.currency_format = currency_data.currency_format
            render_data.currency_decimals = currency_data.currency_decimals
        
        return render_data

class ReportParser:
    @staticmethod
    def setup(parent_subparser):
        report_parser = parent_subparser.add_parser("report", help="Report on a single .budget file.")
        CommonParser.setup_render_options(report_parser)
        report_parser.add_argument("file")
        report_parser.set_defaults(func=ReportParser.report)

    @staticmethod
    def report(args): 
        entries = parse.budget(args.file)
        
        report_data = transform.entries_to_report_data(entries)
        render_data = CommonParser.get_render_options(args)

        render.report(report_data, render_data)

class DiffParser:
    @staticmethod
    def setup(parent_subparser):
        diff_parser = parent_subparser.add_parser("diff", help="See the difference between each category in several .budget files. Each file is considered one time period and differences are rolling between periods.")
        CommonParser.setup_render_options(diff_parser)
        diff_parser.add_argument("files", nargs="+")
        diff_parser.add_argument("--output", choices=["text","csv"], default="text")
        diff_parser.set_defaults(func=DiffParser.diff)

    @staticmethod
    def diff(args):
        render_data = CommonParser.get_render_options(args)
        if len(args.files) < 2:
            raise ValueError("Must have at least 2 files to produce a diff.")

        file_entries = [ parse.budget(filename) for filename in args.files ]
        category_trees = [ transform.generate_category_dict(f) for f in file_entries]
        diff_tree = transform.generate_diff_dict(category_trees)
        names = [ Path(f).stem for f in args.files ]

        if args.output == "text":
            table = render.diff_tree(diff_tree, names, render_data)
            console = Console()
            console.print(table)
        elif args.output == "csv":
            csv_rows = render.diff_csv(diff_tree, names, render_data)
            writer = csv.writer(sys.stdout)
            writer.writerows(csv_rows)

class ConvertParser:
    @staticmethod
    def setup(parent_subparser):
        convert_parser = parent_subparser.add_parser("convert", help="Convert to minibudget format from other financial formats.")
        convert_parser.add_argument("file")
        convert_parser.add_argument("--width", help="Width of the output minibudget in characters. Default is 80.", default=80)
        convert_parser.add_argument("--start", help="Start date to query from, inclusive.")
        convert_parser.add_argument("--end", help="End date to query until, inclusive.")
        convert_parser.add_argument("--currency", help="The currency to convert into minibudget format, where multiple are available. Default is USD.", default="USD")
        convert_parser.add_argument("--format", help="Format of the input file to output as minibudget entries.", choices=["beancount"])
        convert_parser.set_defaults(func=ConvertParser.convert)

    @staticmethod
    def convert(args):
        format = ConvertParser.infer_format(args)
        if format == "beancount":
            entries = convert.beancount(args.file, args.currency, args.start, args.end)
        else:
            raise ValueError(f"{args.file} is not a parseable type.")
        print(convert.entry_list_to_string(entries, int(args.width)))
        
    @staticmethod
    def infer_format(args):
        if args.format is not None:
            return args.format
        file_path = Path(args.file)
        if file_path.suffix == ".beancount":
            return "beancount"
        return None
            
