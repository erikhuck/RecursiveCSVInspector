"""Module for the master handler"""

from argparse import ArgumentParser, Namespace

from handler.extract_handler import ExtractHandler
from strings.args import EXTRACT_HANDLER_NAME, SUB_PARSER


class MasterHandler:
    """The master handler sets up and selects the handler that was specified from the command line"""

    def __init__(self, argv: list):
        parser: ArgumentParser = ArgumentParser()

        subparsers = parser.add_subparsers(dest=SUB_PARSER, title=SUB_PARSER)
        subparsers.required = True

        extract_parser: ArgumentParser = subparsers.add_parser(EXTRACT_HANDLER_NAME)
        ExtractHandler.configure_parser(extract_parser)

        # TODO: ADD PRINT PARSER

        self.args: Namespace = parser.parse_args(argv)

    def handle(self):
        """Determines which handler was specified from the command line and calls that handler"""

        handler_type: str = self.args.handler_type

        # TODO: ADD PRINT HANDLER
        if handler_type == EXTRACT_HANDLER_NAME:
            ExtractHandler.handle(self.args)
