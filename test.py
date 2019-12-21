"""Module ran on the command line which runs all the tests"""

from os import system
import sys
from unittest import TestLoader, TestSuite, TextTestRunner

from strings.general import TEST_DIR, MAIN_NAME

# system('apt install bash')
system('echo $SHELL')
system('SHELL=/bin/bash')
system('echo $SHELL')

if __name__ == MAIN_NAME:
    test_runner: TextTestRunner = TextTestRunner(verbosity=1)
    tests: TestSuite = TestLoader().discover(TEST_DIR)

    success: bool = test_runner.run(tests).wasSuccessful()

    if not success:
        sys.exit(1)
