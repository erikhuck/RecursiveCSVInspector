"""Module for the inspect handler class"""

from argparse import ArgumentParser, Namespace
from collections import Iterable

from handler.handler import Handler
from handler.inspect_handler.csv_object import CSVObject, NominalColumn
from handler.utils import remove_root_dir
from strings.args import (
    KEY_WORDS_ARG, KEY_WORDS_ARG_HELP, STORE_ACTION, STORE_TRUE_ACTION, VERBOSE_ARG, VERBOSE_ARG_HELP
)
from strings.general import CSV_EXTENSION
from strings.inspect_handler import NO_OUTPUT_MSG


class InspectHandler(Handler):
    """Handler fulfilling the main purpose of this repository which is inspecting csv files using key words"""

    _csv_objects: dict = None
    _key_words: list = None
    _data_path: str = None

    @staticmethod
    def configure_parser(parser: ArgumentParser):
        """
        Configures the arguments for the inspect handler

        @param parser: The parser to configure
        """

        Handler.configure_parser(parser)

        parser.add_argument(VERBOSE_ARG, action=STORE_TRUE_ACTION, required=False, help=VERBOSE_ARG_HELP)
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
        assert InspectHandler._data_path is None

        InspectHandler._csv_objects = {}
        InspectHandler._key_words = args.key_words
        InspectHandler._data_path = args.data_path

        Handler._directory_walk(dir_path=args.data_path, action=InspectHandler._inspect_file)

        # Print out all the info in the csv objects
        info: list = InspectHandler._get_info(verbose=args.verbose)
        for output_line in info:
            print(output_line)

    @staticmethod
    def _inspect_file(*args):
        """
        Inspects a file in a directory and collects information about it if it's a csv, else ignores it

        @param args: Contains the file path that may be a csv
        """

        _, file_path = args

        if file_path.endswith(CSV_EXTENSION):
            csv_obj: CSVObject = CSVObject(csv_path=file_path)

            # Remove the root directory from the file path before looking for matches, it being arbitrary and irrelevant
            file_path: str = remove_root_dir(file_path=file_path, root=InspectHandler._data_path)

            assert file_path not in InspectHandler._csv_objects

            # Check for key word matches in the file path
            relevant: bool = InspectHandler._check_matches(potential_matches={file_path})

            # If a key word wasn't in the file path, check the column names
            if not relevant:
                col_names: Iterable = csv_obj.get_csv_col_names()
                relevant: bool = InspectHandler._check_matches(potential_matches=col_names)

            # If a key word wasn't in the column names, check the values of nominal columns
            if not relevant:
                nominal_cols: set = csv_obj.get_nominal_cols()
                for nominal_col in nominal_cols:
                    assert type(nominal_col) is NominalColumn

                    classes: set = nominal_col.get_classes()
                    relevant: bool = InspectHandler._check_matches(potential_matches=classes)

                    if relevant:
                        break

            if relevant:
                InspectHandler._csv_objects[file_path] = csv_obj

    @staticmethod
    def _check_matches(potential_matches: Iterable) -> bool:
        """
        Checks for matches with the key words and a collection of strings

        @param potential_matches: The collection of strings that might contain one of the key words
        @return: Whether there is a match or not
        """

        for kw in InspectHandler._key_words:
            assert type(kw) is str
            kw: str = kw.lower()

            for potential_match in potential_matches:
                assert type(potential_match) is str
                potential_match: str = potential_match.lower()

                if kw in potential_match:
                    return True
        return False

    @staticmethod
    def _get_info(verbose: bool) -> list:
        """
        Creates and returns the information for all the relevant csv files

        @param verbose: Whether to print extra information about the CSV columns rather than just their names
        @return: The list of output lines
        """

        # If there are no relevant CSVs, return the no output message
        if len(InspectHandler._csv_objects) == 0:
            return [NO_OUTPUT_MSG]

        inspect_handler_info: list = []

        # Sort the file paths when collecting the csv info to ensure determinism
        file_paths: list = sorted(InspectHandler._csv_objects.keys())

        for file_path in file_paths:
            csv_obj: CSVObject = InspectHandler._csv_objects[file_path]
            csv_obj_info: list = csv_obj.get_info(verbose=verbose)
            inspect_handler_info.append(file_path)
            inspect_handler_info.extend(csv_obj_info)
        return inspect_handler_info
