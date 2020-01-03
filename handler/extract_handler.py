"""Module for the extract handler class"""

from argparse import Namespace
from os import mkdir, system
from os.path import isdir, isfile, join, split

from handler.handler import Handler
from strings.extract_handler import *


class ExtractHandler(Handler):
    """The handler for extracting all the compressed files in the data directory"""

    @staticmethod
    def handle(args: Namespace):
        """
        Extracts all the compressed files in the data directory so they can be queried

        @param args: The arguments for the extract handler
        """

        Handler._directory_walk(dir_path=args.data_path, action=ExtractHandler._extract_file)

    @staticmethod
    def _extract_file(root: str, file_path: str):
        """
        Extracts a file in a directory

        @param root: The directory that the file is in
        @param file_path: The path to the file to extract
        """

        if file_path.endswith(TAR_GZ_EXTENSION):
            ExtractHandler._extract_tar_gz(file_path=file_path, dest_dir=root)
        elif file_path.endswith(GZ_EXTENSION):
            ExtractHandler._extract_gz(file_path=file_path)
        elif file_path.endswith(TAR_EXTENSION):
            ExtractHandler._extract_tar(file_path=file_path, dest_dir=root)
        elif file_path.endswith(ZIP_EXTENSION):
            ExtractHandler._extract_zip(file_path=file_path, dest_dir=root)

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

        # Get the name of the compressed-directory file to act as the destination of the extracted contents
        file_name: str = ExtractHandler._get_compressed_file_name(file_path=file_path)
        dest_dir: str = join(dest_dir, file_name)

        assert not isdir(dest_dir)
        mkdir(dest_dir)

        command: str = extract_command.format(file_path, dest_dir)
        system(command)

        ExtractHandler._remove_file(file_path)

    @staticmethod
    def _get_compressed_file_name(file_path: str) -> str:
        """
        Gets the name of a compressed file

        @param file_path: The path to the compressed file
        @return: The name of the compressed file
        """

        assert isfile(file_path)

        _, file_name = split(file_path)

        if file_path.endswith(TAR_EXTENSION):
            extension_len: int = len(TAR_EXTENSION)
        elif file_path.endswith(ZIP_EXTENSION):
            extension_len: int = len(ZIP_EXTENSION)
        elif file_path.endswith(TAR_GZ_EXTENSION):
            extension_len: int = len(TAR_GZ_EXTENSION)
        else:
            error_msg: str = FILE_EXTENSION_UNSUPPORTED_MSG.format(file_path)
            raise ValueError(error_msg)

        assert extension_len > 0

        file_name: str = file_name[:len(file_name) - extension_len]
        return file_name

    @staticmethod
    def _remove_file(file_path: str):
        """
        Removes a file from the file system, ensuring the file exists

        @param file_path: The path to the file to remove
        """

        assert isfile(file_path)

        system(REMOVE_FILE_COMMAND.format(file_path))
