"""Module containing the master handler test case class"""

from argparse import Namespace
from unittest import TestCase

from handler.master_handler import MasterHandler
from strings.args import EXTRACT_HANDLER_NAME
from strings.test_data import TEST_DATA_PATH
from test.utils import get_master_handler


class TestMasterHandler(TestCase):
    """Contains tests for the master handler"""

    def test_init(self):
        """Tests that the master handler is initialized properly"""

        master_handler: MasterHandler = get_master_handler(handler_type=EXTRACT_HANDLER_NAME)

        args: Namespace = master_handler.args
        self.assertEqual(args.handler_type, EXTRACT_HANDLER_NAME)
        self.assertEqual(args.data_path, TEST_DATA_PATH)

        # TODO: Add tests for print handler arg parsing
