"""Module containing the inspect handler test case class"""

from unittest import TestCase

from handler.inspect_handler.inspect_handler import InspectHandler
from handler.master_handler import MasterHandler
from strings.args import INSPECT_HANDLER_NAME, TEST_KEY_WORD1, TEST_KEY_WORD2, TEST_KEY_WORD3, TEST_KEY_WORD4
from strings.inspect_handler import NO_OUTPUT_MSG
from strings.test_inspect_handler import *
from test.utils import get_inspect_args, get_master_handler, TestDataCreator


class TestInspectHandler(TestCase):
    """Contains tests for the inspect handler"""

    def test_handle(self):
        """Tests that the inspect handler outputs the correct information about the test data"""

        creator: TestDataCreator = TestDataCreator()

        creator.create_test_data(compress=False)

        """
        Test for non-cap-sensitivity in a file path, a match in a file path, using multiple key words, a column
        consisting entirely of floats, a column consisting of both integers and floats, a column consisting of nominal
        and numeric values, a column consisting of integers and NaNs, a column consisting of floats and NaNs, a column
        consisting of nominal values and NaNs, a column with only NaNs, and test that a CSV's information is not shown
        multiple times even if it gets a match in multiple ways
        """
        key_words: list = [TEST_KEY_WORD1, TEST_KEY_WORD2]
        expected_output: list = TestInspectHandler._get_expected_output(csv1=False, csv2=True, csv3=True)
        self._run_handler(key_words=key_words, expected_output=expected_output)

        """
        Test for non-cap-sensitivity in column names and nominal values, matches in column names and nominal values,
        using a single key word, a column entirely consisting of integers, a nominal column with differing value-counts,
        a nominal column with all the same value, and a nominal column with integers, floats, nominal values, and NaNs
        """
        key_words: list = [TEST_KEY_WORD3]
        expected_output: list = TestInspectHandler._get_expected_output(csv1=True, csv2=False, csv3=True)
        self._run_handler(key_words=key_words, expected_output=expected_output)

        # Test for getting no relevant CSVs
        key_words: list = [TEST_KEY_WORD4]
        expected_output: list = TestInspectHandler._get_expected_output(csv1=False, csv2=False, csv3=False)

        # Test for a data path with a trailing slash
        self._run_handler(key_words=key_words, expected_output=expected_output, trailing_slash=True)

        creator.destroy_test_data()

    def _run_handler(self, key_words: list, expected_output: list, trailing_slash: bool = False):
        """
        Runs the inspect handler and tests the output for a given list of key words

        @param key_words: The key words for the inspect handler
        @param expected_output: The output to check against
        @param trailing_slash: Whether the test data directory path has a trailing slash at the end of it
        """

        # Reset the inspect handler
        InspectHandler._csv_objects = None
        InspectHandler._key_words = None
        InspectHandler._data_path = None

        argv: list = get_inspect_args(key_words=key_words)
        master_handler: MasterHandler = get_master_handler(
            handler_type=INSPECT_HANDLER_NAME, extra_args=argv, trailing_slash=trailing_slash
        )
        master_handler.handle()

        actual_output: list = InspectHandler._get_info()
        self.assertEqual(actual_output, expected_output)

    @staticmethod
    def _get_expected_output(csv1: bool, csv2: bool, csv3: bool) -> list:
        """
        Returns the entire expected output of a test case

        @param csv1: Whether the first test CSV was relevant
        @param csv2: Whether the second test CSV was relevant
        @param csv3: Whether the third test CSV was relevant
        @return: The list of all the output lines
        """

        if not csv1 and not csv2 and not csv3:
            return [NO_OUTPUT_MSG]

        expected_output: list = []

        if csv1:
            expected_output.extend(TestInspectHandler._get_csv1_output())

        if csv2:
            expected_output.extend(TestInspectHandler._get_csv2_output())

        if csv3:
            expected_output.extend(TestInspectHandler._get_csv3_output())

        return expected_output

    @staticmethod
    def _get_csv1_output() -> list:
        """
        Returns the output lines for the first test csv

        @return: The list of output lines
        """

        return [
            CSV1_LINE1, CSV1_LINE2, CSV1_LINE3, CSV1_LINE4, CSV1_LINE5, CSV1_LINE6, CSV1_LINE7, CSV1_LINE8, CSV1_LINE9,
            CSV1_LINE10, CSV1_LINE11, CSV1_LINE12, CSV1_LINE13, CSV1_LINE14, CSV1_LINE15, CSV1_LINE16, CSV1_LINE17
        ]

    @staticmethod
    def _get_csv2_output() -> list:
        """
        Returns the output lines for the second test csv

        @return: The list of output lines
        """

        return [
            CSV2_LINE1, CSV2_LINE2, CSV2_LINE3, CSV2_LINE4, CSV2_LINE5, CSV2_LINE6, CSV2_LINE7, CSV2_LINE8, CSV2_LINE9,
            CSV2_LINE10, CSV2_LINE11, CSV2_LINE12, CSV2_LINE13, CSV2_LINE14, CSV2_LINE15, CSV2_LINE16, CSV2_LINE17,
            CSV2_LINE18, CSV2_LINE19
        ]

    @staticmethod
    def _get_csv3_output() -> list:
        """
        Returns the output lines for the third test csv

        @return: The list of output lines
        """

        return [
            CSV3_LINE1, CSV3_LINE2, CSV3_LINE3, CSV3_LINE4, CSV3_LINE5, CSV3_LINE6, CSV3_LINE7, CSV3_LINE8, CSV3_LINE9,
            CSV3_LINE10, CSV3_LINE11, CSV3_LINE12, CSV3_LINE13, CSV3_LINE14, CSV3_LINE15, CSV3_LINE16, CSV3_LINE17,
            CSV3_LINE18, CSV3_LINE19
        ]
