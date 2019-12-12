"""Module ran on the command line which runs all the tests"""

import sys
from unittest import TestLoader, TestSuite, TextTestRunner

from strings.general import TEST_DIR, MAIN_NAME


def _create_test_data():
    # TODO: Create the directory used to test
    pass


def _destroy_test_data():
    # TODO: Destroy the test directory
    pass


if __name__ == MAIN_NAME:
    test_runner: TextTestRunner = TextTestRunner(verbosity=1)
    tests: TestSuite = TestLoader().discover(TEST_DIR)

    _create_test_data()

    success: bool = test_runner.run(tests).wasSuccessful()

    _destroy_test_data()

    if not success:
        sys.exit(1)
