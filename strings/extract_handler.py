"""Module containing strings used by the extract handler"""

FILE_EXTENSION_UNSUPPORTED_MSG: str = 'The file extension of the file {} cannot be extracted'
GZ_EXTRACT_COMMAND: str = 'gunzip {}'
GZ_EXTENSION: str = '.gz'
REMOVE_FILE_COMMAND: str = 'rm {}'
TAR_EXTRACT_COMMAND: str = 'tar -xf {} -C {}'
TAR_EXTENSION: str = '.tar'
TAR_GZ_EXTENSION: str = '.tar.gz'
TAR_GZ_EXTRACT_COMMAND: str = 'tar -xzf {} -C {}'
ZIP_EXTENSION: str = '.zip'
ZIP_EXTRACT_COMMAND: str = 'unzip {} -d {} > /dev/null'
