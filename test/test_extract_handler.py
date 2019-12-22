"""Module containing the extract handler test case class"""

from os.path import isdir, isfile
from unittest import TestCase

from handler.master_handler import MasterHandler
from strings.args import EXTRACT_HANDLER_NAME
from test.utils import TestDataCreator, get_master_handler


class TestExtractHandler(TestCase):
    """Contains a test for the extract handler"""

    def test_handle(self):
        """Tests that the extract handler properly extracts all the compressed files and directories in the test data"""

        creator: TestDataCreator = TestDataCreator()
        creator.create_test_data(compress=True)
        test_data_paths: set = creator.get_test_data_paths()

        master_handler: MasterHandler = get_master_handler(handler_type=EXTRACT_HANDLER_NAME)
        master_handler.handle()

        self._verify_test_data(test_data_paths)

        creator.destroy_test_data()

    def _verify_test_data(self, test_data_paths: set):
        """
        Tests that all the directories and files were successfully extracted

        @param test_data_paths: The set of paths to the files and directories which should exist after extracting
        """

        for path in test_data_paths:
            path_exists: bool = TestExtractHandler._path_exists(path=path)
            self.assertTrue(path_exists)

    @staticmethod
    def _path_exists(path: str) -> bool:
        """
        Determines whether a string corresponds to an existing path to a file or directory

        @param path: The path to test
        @return: The truth value of the query
        """

        return isdir(path) or isfile(path)
