"""Module for the extract handler class"""

from argparse import Namespace
from os import walk, system
from os.path import join

from handler.handler import Handler
from strings.extract_handler import (
    GZ_COMMAND, GZ_EXTENSION, TAR_COMMAND, TAR_EXTENSION, TAR_GZ_COMMAND, REMOVE_FILE_COMMAND, ZIP_COMMAND,
    ZIP_EXTENSION
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
        for root, directories, files in walk(path):
            for file in files:
                file_path: str = join(root, file)

                if GZ_EXTENSION in file_path:
                    ExtractHandler._extract_gz(file_path, root)
                elif TAR_EXTENSION in file_path:
                    ExtractHandler._extract_tar(file_path, root)
                elif ZIP_EXTENSION in file_path:
                    ExtractHandler._extract_zip(file_path)

                system(REMOVE_FILE_COMMAND.format(file_path))

            # TODO: After extracting all the directories in the current directory, recursively extract within them

    @staticmethod
    def _extract_gz(file_path: str, dest_dir: str):
        if TAR_EXTENSION in file_path:
            ExtractHandler._extract_tar_gz(file_path, dest_dir)
        else:
            command: str = TAR_COMMAND.format(file_path, dest_dir)
            system(command)

    @staticmethod
    def _extract_tar(file_path: str, dest_dir: str):
        if GZ_EXTENSION in file_path:
            ExtractHandler._extract_tar_gz(file_path, dest_dir)
        else:
            command: str = GZ_COMMAND.format(file_path)
            system(command)

    @staticmethod
    def _extract_zip(file_path: str):
        unzipped_dir: str = file_path.split(ZIP_EXTENSION)[0]
        command: str = ZIP_COMMAND.format(file_path, unzipped_dir)
        system(command)

    @staticmethod
    def _extract_tar_gz(file_path, dest_dir: str):
        command: str = TAR_GZ_COMMAND.format(file_path, dest_dir)
        system(command)
