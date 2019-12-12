"""Module for test case which tests the master handler"""

from argparse import Namespace
from unittest import TestCase

from handler.master_handler import MasterHandler
from strings.handler import DATA_PATH_ARG, EXTRACT_HANDLER_NAME
from strings.test import TEST_DATA_PATH


class TestMasterHandler(TestCase):

    def test_init(self):
        argv: list = self._get_test_argv(handler_type=EXTRACT_HANDLER_NAME)
        master_handler: MasterHandler = MasterHandler(argv)

        args: Namespace = master_handler.args
        self.assertEqual(args.handler_type, EXTRACT_HANDLER_NAME)
        self.assertEqual(args.data_path, TEST_DATA_PATH)

    @staticmethod
    def _get_test_argv(handler_type: str):
        argv: list = [
            handler_type,
            DATA_PATH_ARG, TEST_DATA_PATH
        ]
        return argv
