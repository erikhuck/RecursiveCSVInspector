"""Module for the handler base class"""

from argparse import ArgumentParser, Namespace
from os import walk
from os.path import isdir, join

from strings.args import DATA_PATH_ARG, DATA_PATH_ARG_HELP, STORE_ACTION


class Handler:
    """A base class for all the handlers. The type of handler is specified as a command line argument"""

    @staticmethod
    def configure_parser(parser: ArgumentParser):
        """
        Configures the base arguments that apply to all handlers that extend the handler base class

        @param parser: The parser to add the base arguments to
        """

        parser.add_argument(DATA_PATH_ARG, type=str, action=STORE_ACTION, required=True, help=DATA_PATH_ARG_HELP)

    @staticmethod
    def handle(args: Namespace):
        """
        All handlers have a handle function which performs their functionality

        @param args: The arguments for the handler which affect their functionality
        """

        raise NotImplementedError()

    @staticmethod
    def _directory_walk(dir_path: str, action: callable):
        """
        Recursively walks through each file in a directory and its subdirectories, performing some action on them

        @param dir_path: The path to the current directory in the current level of recursion
        @param action: The action to perform on the files of the current directory
        """

        assert isdir(dir_path)

        for root, _, files in walk(dir_path):
            for file in files:
                file_path: str = join(root, file)
                action(root, file_path)
            break

        for root, directories, _ in walk(dir_path):
            for directory in directories:
                recursive_path: str = join(dir_path, directory)
                Handler._directory_walk(dir_path=recursive_path, action=action)
            break
