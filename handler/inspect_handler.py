"""Module for the inspect handler class"""

from argparse import ArgumentParser, Namespace

from handler.handler import Handler
from strings.args import KEY_WORDS_ARG, KEY_WORDS_ARG_HELP, STORE_ACTION


class InspectHandler(Handler):
    """Handler fulfilling the main purpose of this repository which is inspecting csv files using key words"""

    @staticmethod
    def configure_parser(parser: ArgumentParser):
        """
        Configures the arguments for the inspect handler

        @param parser: The parser to configure
        """

        Handler.configure_parser(parser)

        parser.add_argument(KEY_WORDS_ARG, nargs='+', action=STORE_ACTION, required=True, help=KEY_WORDS_ARG_HELP)

    @staticmethod
    def handle(args: Namespace):
        """
        Recursively looks through a directory and its sub directories searching for key words in csv files and their
        file paths

        @param args: The arguments for the inspect handler, including key words to search for
        """

        pass
