"""Module containing the master handler test case class"""

from argparse import Namespace
from unittest import TestCase

from handler.master_handler import MasterHandler
from strings.args import EXTRACT_HANDLER_NAME, INSPECT_HANDLER_NAME, TEST_KEY_WORD1, TEST_KEY_WORD2
from strings.test_data import TEST_DATA_PATH
from test.utils import get_inspect_args, get_master_handler


class TestMasterHandler(TestCase):
    """Contains tests for the master handler"""

    def test_init(self):
        """Tests that the master handler is initialized properly"""

        # Test that the extract handler arguments are initialized properly
        master_handler: MasterHandler = get_master_handler(handler_type=EXTRACT_HANDLER_NAME)
        self._assert_base_args(master_handler=master_handler, handler_name=EXTRACT_HANDLER_NAME)

        # Test that the inspect handler arguments are initialized properly
        key_words: list = [TEST_KEY_WORD1, TEST_KEY_WORD2]
        n_key_words: int = len(key_words)
        inspect_args = get_inspect_args(key_words=key_words)
        master_handler: MasterHandler = get_master_handler(handler_type=INSPECT_HANDLER_NAME, extra_args=inspect_args)
        args: Namespace = self._assert_base_args(master_handler=master_handler, handler_name=INSPECT_HANDLER_NAME)
        key_words: list = args.key_words
        self.assertEqual(type(key_words), list)
        self.assertEqual(len(key_words), n_key_words)
        self.assertTrue(TEST_KEY_WORD1 in key_words)
        self.assertTrue(TEST_KEY_WORD2 in key_words)

    def _assert_base_args(self, master_handler: MasterHandler, handler_name: str) -> Namespace:
        """
        Tests that the arguments relevant to all handlers are initialized properly

        @param master_handler: The master handler which parsed the arguments for the given handler
        @param handler_name: The name of the given handler
        @return: The arguments parsed by the master handler
        """

        args: Namespace = master_handler.args
        self.assertEqual(args.handler_type, handler_name)
        self.assertEqual(args.data_path, TEST_DATA_PATH)
        return args
