"""Module containing functionality used for a number of different tests"""

from os import chdir, getcwd, mkdir, system
from os.path import isdir, isfile, join, realpath, split
from pandas import DataFrame

from handler.master_handler import MasterHandler
from strings.extract_handler import TAR_EXTENSION
from strings.args import DATA_PATH_ARG
from strings.general import CSV_EXTENSION
from strings.test_data import (
    CSV1_NAME, CSV1_NOMINAL_FEAT1_NAME, CSV1_NOMINAL_FEAT1_VAL1, CSV1_NOMINAL_FEAT1_VAL2, CSV1_NOMINAL_FEAT1_VAL3,
    CSV1_NOMINAL_FEAT2_NAME, CSV1_NOMINAL_FEAT2_VAL, CSV1_REAL_FEAT_NAME, CSV1_REAL_FEAT_VAL1, CSV1_REAL_FEAT_VAL2,
    CSV1_REAL_FEAT_VAL3, CSV1_REAL_FEAT_VAL4, CSV2_NAME, CSV3_NAME, DIR1_NAME, DIR2_NAME, DIR2A_NAME, DIR2A1_NAME,
    DIR3_NAME, DIR3A_NAME, EMPTY_DIR_NAME, GZ_COMPRESS_COMMAND, REMOVE_DIR_COMMAND, TAR_COMPRESS_COMMAND,
    TEST_DATA_PATH, TXT_EXTENSION, TXT1_NAME, TXT2_NAME, ZIP_COMPRESS_COMMAND
)


class TestDataCreator:
    """Contains the functionality of creating, compressing, and destroying the data used for testing"""

    def __init__(self):
        self._test_data_paths: set = set()

    def get_test_data_paths(self) -> set:
        """
        Returns the paths of all the files and directories created for testing, ensuring they have already been created

        @return: The test data paths
        """

        assert len(self._test_data_paths) > 0

        return self._test_data_paths

    def create_test_data(self, compress: bool):
        """
        Creates a test data directory containing files and sub directories which act as the data to run tests on

        @param compress: Whether to compress some of the files and directories in the test data
        """

        if isdir(TEST_DATA_PATH):
            self.destroy_test_data()

        mkdir(TEST_DATA_PATH)

        csv1: DataFrame = DataFrame(
            {
                CSV1_NOMINAL_FEAT1_NAME: [
                    CSV1_NOMINAL_FEAT1_VAL1, CSV1_NOMINAL_FEAT1_VAL3, CSV1_NOMINAL_FEAT1_VAL2, CSV1_NOMINAL_FEAT1_VAL2,
                    CSV1_NOMINAL_FEAT1_VAL3, CSV1_NOMINAL_FEAT1_VAL2
                ],
                CSV1_NOMINAL_FEAT2_NAME: [
                    CSV1_NOMINAL_FEAT2_VAL, CSV1_NOMINAL_FEAT2_VAL, CSV1_NOMINAL_FEAT2_VAL, CSV1_NOMINAL_FEAT2_VAL,
                    CSV1_NOMINAL_FEAT2_VAL, CSV1_NOMINAL_FEAT2_VAL
                ],
                CSV1_REAL_FEAT_NAME: [
                    CSV1_REAL_FEAT_VAL1, CSV1_REAL_FEAT_VAL3, CSV1_REAL_FEAT_VAL3, CSV1_REAL_FEAT_VAL4,
                    CSV1_REAL_FEAT_VAL3, CSV1_REAL_FEAT_VAL2
                ]
            }
        )

        csv1_path: str = join(TEST_DATA_PATH, CSV1_NAME + CSV_EXTENSION)
        csv1.to_csv(csv1_path)
        self._test_data_paths.add(csv1_path)

        dir1_paths: set = TestDataCreator._make_dir1(compress=compress)
        self._test_data_paths.update(dir1_paths)
        dir2_paths: set = TestDataCreator._make_dir2(compress=compress)
        self._test_data_paths.update(dir2_paths)
        dir3_paths: set = TestDataCreator._make_dir3(compress=compress)
        self._test_data_paths.update(dir3_paths)

    @staticmethod
    def _make_dir1(compress: bool) -> set:
        """
        Makes the first directory in the test data

        @param compress: Whether to compress the resulting directory
        @return: The set of paths to the resulting directory and its contents
        """

        dir1_paths: set = set()

        dir1_path: str = join(TEST_DATA_PATH, DIR1_NAME)
        dir1_paths.add(dir1_path)
        mkdir(dir1_path)
        empty_dir_path: str = join(dir1_path, EMPTY_DIR_NAME)
        dir1_paths.add(empty_dir_path)
        mkdir(empty_dir_path)

        if compress:
            TestDataCreator._compress_tar_gz(dir_path=dir1_path, dest_dir=TEST_DATA_PATH)

        return dir1_paths

    @staticmethod
    def _make_dir2(compress: bool) -> set:
        """
        Makes the second directory in the test data

        @param compress: Whether to compress the resulting directory and some of its contents
        @return: The set of paths to the resulting directory and its contents
        """

        dir2_paths: set = set()

        dir2_path: str = join(TEST_DATA_PATH, DIR2_NAME)
        dir2_paths.add(dir2_path)
        mkdir(dir2_path)

        dir2a_path: str = join(dir2_path, DIR2A_NAME)
        dir2_paths.add(dir2a_path)
        mkdir(dir2a_path)

        csv2_path: str = join(dir2a_path, CSV2_NAME + CSV_EXTENSION)
        dir2_paths.add(csv2_path)
        # TODO: Fill in data frame
        csv2: DataFrame = DataFrame({})
        csv2.to_csv(csv2_path)

        dir2a1_path: str = join(dir2a_path, DIR2A1_NAME)
        dir2_paths.add(dir2a1_path)
        mkdir(dir2a1_path)

        txt1_path: str = join(dir2a1_path, TXT1_NAME + TXT_EXTENSION)
        dir2_paths.add(txt1_path)
        open(txt1_path, 'w')

        if compress:
            TestDataCreator._compress_gz(txt1_path)
            TestDataCreator._compress_tar_gz(dir_path=dir2a_path, dest_dir=dir2_path)
            TestDataCreator._compress_zip(dir_path=dir2_path, dest_dir=TEST_DATA_PATH)

        return dir2_paths

    @staticmethod
    def _make_dir3(compress: bool) -> set:
        """
        Makes the third directory in the test data

        @param compress: Whether to compress the resulting directory and some of its contents
        @return: The set of paths to the resulting directory and its contents
        """

        dir3_paths: set = set()

        dir3_path: str = join(TEST_DATA_PATH, DIR3_NAME)
        dir3_paths.add(dir3_path)
        mkdir(dir3_path)

        txt2_path: str = join(dir3_path, TXT2_NAME + TXT_EXTENSION)
        dir3_paths.add(txt2_path)
        open(txt2_path, 'w')

        dir3a_path: str = join(dir3_path, DIR3A_NAME)
        dir3_paths.add(dir3a_path)
        mkdir(dir3a_path)

        csv3_path: str = join(dir3a_path, CSV3_NAME + CSV_EXTENSION)
        dir3_paths.add(csv3_path)
        # TODO: Fill in data frame
        csv3: DataFrame = DataFrame({})
        csv3.to_csv(csv3_path)

        if compress:
            TestDataCreator._compress_gz(csv3_path)
            TestDataCreator._compress_zip(dir_path=dir3a_path, dest_dir=dir3_path)
            TestDataCreator._compress_tar(dir_path=dir3_path, dest_dir=TEST_DATA_PATH)

        return dir3_paths

    @staticmethod
    def _compress_gz(file_path: str):
        """
        Compresses a file with a .gz extension

        @param file_path: The path to the file to compress
        """

        assert isfile(file_path)

        command: str = GZ_COMPRESS_COMMAND.format(file_path)
        system(command)

    @staticmethod
    def _compress_zip(dir_path: str, dest_dir: str):
        """
        Compresses a directory as a .zip file

        @param dir_path: The path to the directory to compress
        @param dest_dir: The path to the directory to place the resulting .zip file
        """

        TestDataCreator._compress_dir(
            dir_path=dir_path, dest_dir=dest_dir, compress_command=ZIP_COMPRESS_COMMAND
        )

    @staticmethod
    def _compress_tar(dir_path: str, dest_dir: str):
        """
        Compresses a directory as a .tar file
        @param dir_path: The path to the directory to compress
        @param dest_dir: The path to the directory to place the resulting .tar file
        """

        TestDataCreator._compress_dir(
            dir_path=dir_path, dest_dir=dest_dir, compress_command=TAR_COMPRESS_COMMAND
        )

    @staticmethod
    def _compress_tar_gz(dir_path: str, dest_dir: str):
        """
        Compresses a directory with as a .tar.gz file

        @param dir_path: The path to the directory to compress
        @param dest_dir: Path to the directory to place the resulting .tar.gz file
        """

        TestDataCreator._compress_tar(dir_path=dir_path, dest_dir=dest_dir)
        tar_file_path: str = dir_path + TAR_EXTENSION
        TestDataCreator._compress_gz(file_path=tar_file_path)

    @staticmethod
    def _compress_dir(dir_path: str, dest_dir: str, compress_command: str):
        """
        Compresses a directory

        @param dir_path: The path to the directory to compress
        @param dest_dir: Path to the directory to place the resulting compressed-directory file
        @param compress_command: The terminal-command which specifies the extension of the compressed-directory file
        """

        assert isdir(dir_path)
        assert isdir(dest_dir)

        dir_name: str = split(dir_path)[-1]
        command: str = compress_command.format(dir_name)

        with NewWorkingDir(new_working_dir=dest_dir):
            system(command)

        TestDataCreator._remove_dir(dir_path=dir_path)

    @staticmethod
    def _remove_dir(dir_path: str):
        """
        Removes the directory in the given path, ensuring that the path leads to a directory that exists

        @param dir_path: The path of the directory to remove
        """

        assert isdir(dir_path)

        command: str = REMOVE_DIR_COMMAND.format(dir_path)
        system(command)

    def destroy_test_data(self):
        """Removes all the files and folders that are part of the data created for testing"""

        TestDataCreator._remove_dir(dir_path=TEST_DATA_PATH)
        self._test_data_paths: set = set()


class NewWorkingDir:
    """A context that changes the working directory upon entering and restores the working directory upon exiting"""

    def __init__(self, new_working_dir: str):
        assert isdir(new_working_dir)

        self._old_working_dir: str = getcwd()
        self._new_working_dir: str = realpath(new_working_dir)

    def __enter__(self):
        """Changes the working directory to the new working directory"""

        chdir(self._new_working_dir)

    def __exit__(self, *args):
        """Changes the working directory back to the original working directory"""

        chdir(self._old_working_dir)


def get_master_handler(handler_type: str) -> MasterHandler:
    """
    Creates a master handler with the given handler type, for the purpose of testing

    @param handler_type: The type of handler for the master handler to run
    @return: The master handler
    """

    argv: list = [
        handler_type,
        DATA_PATH_ARG, TEST_DATA_PATH
    ]

    return MasterHandler(argv)
