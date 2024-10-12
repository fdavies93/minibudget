from minibudget import parse
from minibudget import render
from minibudget import transform
from minibudget.render import RenderOptions

class CommonParser:
    @staticmethod
    def setup_render_options(parser):
        parser.add_argument("--width", type=int, default=80)
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
        if args.width <= 0:
            raise ValueError("Display width must be more than 0.")

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
        diff_parser.set_defaults(func=DiffParser.diff)

    @staticmethod
    def diff(args):
        render_data = CommonParser.get_render_options(args)
        if len(args.files) < 2:
            raise ValueError("Must have at least 2 files to produce a diff.")

        file_entries = [ parse.budget(filename) for filename in args.files ]
        
