"""Module for the handler base class"""

from argparse import ArgumentParser, Namespace

from strings.args import DATA_PATH_ARG, DATA_PATH_ARG_HELP, STORE_ACTION


class Handler:
    """A base class for all the handlers. The type of handler is specified as a command line argument"""

    @staticmethod
    def configure_parser(parser: ArgumentParser):
        """
        Configures the base arguments that apply to all handlers that extend the handler base class
        @param parser: The parser to add the base arguments to
        """
        parser.add_argument(DATA_PATH_ARG, type=str, action=STORE_ACTION, help=DATA_PATH_ARG_HELP)

    @staticmethod
    def handle(args: Namespace):
        """
        All handlers have a handle function which performs their functionality
        @param args: The arguments for the handler which affect their functionality
        """
        raise NotImplementedError()
