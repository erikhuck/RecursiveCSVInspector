"""Module for the inspect handler class"""

from argparse import ArgumentParser, Namespace

from handler.handler import Handler
from handler.inspect_handler.csv_object import CSVObject
from strings.args import KEY_WORDS_ARG, KEY_WORDS_ARG_HELP, STORE_ACTION
from strings.general import CSV_EXTENSION


class InspectHandler(Handler):
    """Handler fulfilling the main purpose of this repository which is inspecting csv files using key words"""

    _csv_objects: dict = None
    _key_words: list = None

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

        assert InspectHandler._csv_objects is None
        assert InspectHandler._key_words is None

        InspectHandler._csv_objects = {}
        InspectHandler._key_words = args.key_words

        Handler._directory_walk(dir_path=args.data_path, action=InspectHandler._inspect_file)

        # TODO: Print out all the info in the csv objects

    @staticmethod
    def _inspect_file(*args):
        """
        Inspects a file in a directory and collects information about it if it's a csv, else ignores it

        @param args: Contains the file path that may be a csv
        """

        _, file_path = args

        if file_path.endswith(CSV_EXTENSION):
            assert file_path not in InspectHandler._csv_objects

            InspectHandler._csv_objects[file_path] = CSVObject(csv_path=file_path)
