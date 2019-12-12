"""Module for test cases which test modules in the handler package"""

from argparse import Namespace
from unittest import TestCase

from handler.master_handler import MasterHandler
from strings.args import DATA_PATH_ARG, EXTRACT_HANDLER_NAME
from strings.test import TEST_DATA_PATH


def _get_master_handler(handler_type: str):
    argv: list = [
        handler_type,
        DATA_PATH_ARG, TEST_DATA_PATH
    ]

    return MasterHandler(argv)


class TestMasterHandler(TestCase):

    def test_init(self):
        master_handler: MasterHandler = _get_master_handler(handler_type=EXTRACT_HANDLER_NAME)

        args: Namespace = master_handler.args
        self.assertEqual(args.handler_type, EXTRACT_HANDLER_NAME)
        self.assertEqual(args.data_path, TEST_DATA_PATH)

        # TODO: Add tests for print handler arg parsing


class TestExtractHandler(TestCase):

    def test_handle(self):
        master_handler: MasterHandler = _get_master_handler(handler_type=EXTRACT_HANDLER_NAME)
        master_handler.handle()

        # TODO: Add assert statements


# TODO: Add test case for print handler
