"""Module for the extract handler class"""

from argparse import Namespace
from os import walk, system
from os.path import isdir, isfile, join

from handler.handler import Handler
from strings.extract_handler import (
    GZ_EXTRACT_COMMAND, GZ_EXTENSION, TAR_EXTRACT_COMMAND, TAR_EXTENSION, TAR_GZ_EXTRACT_COMMAND, REMOVE_FILE_COMMAND,
    ZIP_EXTRACT_COMMAND, ZIP_EXTENSION
)


class ExtractHandler(Handler):
    """The handler for extracting all the compressed files in the data directory"""

    @staticmethod
    def handle(args: Namespace):
        """
        Extracts all the compressed files in the data directory so they can be queried

        @param args: The arguments for the extract handler
        """

        ExtractHandler._extract_files_in_directory(args.data_path)

    @staticmethod
    def _extract_files_in_directory(path: str):
        """
        Recursively extracts the files and sub-directories of the current directory

        @param path: The path to the current directory in the current level of recursion
        """

        assert isdir(path)

        for root, _, files in walk(path):
            for file in files:
                file_path: str = join(root, file)

                if GZ_EXTENSION in file_path and TAR_EXTENSION in file_path:
                    ExtractHandler._extract_tar_gz(file_path=file_path, dest_dir=root)
                elif GZ_EXTENSION in file_path:
                    ExtractHandler._extract_gz(file_path=file_path)
                elif TAR_EXTENSION in file_path:
                    ExtractHandler._extract_tar(file_path=file_path, dest_dir=root)
                elif ZIP_EXTENSION in file_path:
                    ExtractHandler._extract_zip(file_path=file_path, dest_dir=root)
            break

        for root, directories, _ in walk(path):
            for directory in directories:
                recursive_path: str = join(path, directory)
                ExtractHandler._extract_files_in_directory(recursive_path)
            break

    @staticmethod
    def _extract_gz(file_path: str):
        """
        Extracts a file with a .gz extension

        @param file_path: Path to the .gz file to be extracted
        """

        assert isfile(file_path)

        command: str = GZ_EXTRACT_COMMAND.format(file_path)
        system(command)

    @staticmethod
    def _extract_tar(file_path: str, dest_dir: str):
        """
        Extracts a directory with a .tar extension and removes it

        @param file_path: The path to the .tar file to extract and remove
        @param dest_dir: The destination of the resulting extracted directory
        """

        ExtractHandler._extract_dir(file_path=file_path, dest_dir=dest_dir, extract_command=TAR_EXTRACT_COMMAND)

    @staticmethod
    def _extract_zip(file_path: str, dest_dir):
        """
        Extracts a file with a .zip extension and removes it

        @param file_path: The path to the .zip file to extract and remove
        @param dest_dir: The destination of the resulting extracted directory
        """

        ExtractHandler._extract_dir(file_path=file_path, dest_dir=dest_dir, extract_command=ZIP_EXTRACT_COMMAND)

    @staticmethod
    def _extract_tar_gz(file_path, dest_dir: str):
        """
        Extracts a file with a .tar.gz extension and removes it

        @param file_path: The path to the .tar.gz file to extract and remove
        @param dest_dir: The destination of the resulting extracted directory
        """

        ExtractHandler._extract_dir(file_path=file_path, dest_dir=dest_dir, extract_command=TAR_GZ_EXTRACT_COMMAND)

    @staticmethod
    def _extract_dir(file_path: str, dest_dir: str, extract_command: str):
        """
        Extracts a compressed-directory and removes its corresponding compressed-directory file

        @param file_path: The path to the compressed-directory file to extract and remove
        @param dest_dir: The destination of the resulting extracted directory
        @param extract_command: The terminal-command specifying the extension of the resulting compressed-directory file
        """

        assert isfile(file_path)
        assert isdir(dest_dir)

        command: str = extract_command.format(file_path, dest_dir)
        system(command)
        ExtractHandler._remove_file(file_path)

    @staticmethod
    def _remove_file(file_path: str):
        """
        Removes a file from the file system, ensuring the file exists

        @param file_path: The path to the file to remove
        """

        assert isfile(file_path)

        system(REMOVE_FILE_COMMAND.format(file_path))
