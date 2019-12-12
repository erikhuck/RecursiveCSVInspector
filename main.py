"""The main module that is ran on the command line"""

from sys import argv

from handler.master_handler import MasterHandler
from strings.general import MAIN_NAME


def main():
    """Just creates the master handler and calls it"""

    master_handler: MasterHandler = MasterHandler(argv[1:])
    master_handler.handle()


if __name__ == MAIN_NAME:
    main()
