"""Module for the extract handler class"""

from argparse import Namespace

from handler.handler import Handler


class ExtractHandler(Handler):
    """The handler for extracting all the compressed files in the data directory"""

    @staticmethod
    def handle(args: Namespace):
        """
        Extracts all the compressed files in the data directory so they can be queried
        @param args: The arguments for the extract handler
        """
        pass
