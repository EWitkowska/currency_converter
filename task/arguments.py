import argparse
import sys


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Currency Conversion Script")
        self.add_arguments()

    def add_arguments(self):
        self.parser.add_argument(
            "--mode",
            choices=["dev", "prod"],
            required=True,
            help="Specify the mode (dev or prod)",
        )
        self.parser.add_argument(
            "--source",
            choices=["local", "api"],
            required=True,
            help="Specify the data source (local or api)",
        )

    def parse_arguments(self) -> argparse.Namespace:
        args: argparse.Namespace = self.parser.parse_args()

        if not (args.source and args.mode):
            self.parser.print_usage()
            sys.exit(1)

        return args
