import csv
from os import stat
import sys
from minibudget import parse
from minibudget import render
from minibudget import transform
from minibudget import convert
from minibudget.render import RenderOptions
from rich.console import Console
from pathlib import Path
from plotly import subplots
import plotly.graph_objects as go

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

class ChartParser:
    @staticmethod
    def setup(parent_subparser):
        chart_parser = parent_subparser.add_parser("chart",help="Generate charts based on minibudget files.")
        chart_parser.add_argument("type", choices=["sunburst"]) 
        chart_parser.add_argument("file")
        chart_parser.set_defaults(func=ChartParser.chart)

    @staticmethod
    def chart(args):
        method_dict = {
            "donut": ChartParser.donut,
            "sunburst": ChartParser.sunburst
        }
        method_dict[args.type](args)

    @staticmethod
    def donut(args):
        if len(args.files) > 1:
            raise ValueError("Donut charts must be generated from a single file.")
        entries = parse.budget(args.file)
        expense_entries = list(filter(lambda e: not e.is_income, entries))
        expense_dict = transform.generate_simple_dict(expense_entries)
        layout = subplots.make_subplots(specs=[[{"type":"pie"}]])
        total_expenses = sum(expense_dict.values())
        layout.add_pie(
                       title={"text": f"Expenses\n{total_expenses}"},
                       labels=list(expense_dict.keys()),
                       values=list(expense_dict.values()),
                       hole=0.3,
                       row=1,
                       col=1,
                       sort=False,
                       textinfo="label+value"
                       )
        layout.show()

    @staticmethod
    def sunburst(args):
        entries = parse.budget(args.file)
        expense_entries = list(filter(lambda e: not e.is_income, entries))
        parent_list, label_list, value_list = transform.generate_triple_list(expense_entries)
        burst = go.Figure(go.Sunburst(
            labels=label_list, 
            values=value_list, 
            parents=parent_list, 
            branchvalues="total",
            textinfo="label",
            hoverinfo="label+value+percent entry"
        ))
        burst.show()

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
        diff_parser.add_argument("--output", choices=["text","csv","html"], default="text")
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
        elif args.output == "html":
            page: str = render.diff_html(diff_tree, names, render_data)
            print(page)

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
            
