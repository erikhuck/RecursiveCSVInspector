"""Module containing functionality used across the repository"""

from os.path import isdir, join, split

from strings.general import EMPTY_STRING


def add_trailing_slash(dir_path: str) -> str:
    """
    Adds a trailing slash to a directory path

    @param dir_path: The path to the directory
    @return: The directory path with a slash at the end of it
    """

    assert isdir(dir_path)

    return join(dir_path, EMPTY_STRING)


def remove_root_dir(file_path: str, root: str) -> str:
    """
    Removes the root directory from a file path

    @param file_path: The file path to remove the root directory from
    @param root: The root directory in the path to remove
    @return: The modified file path
    """

    assert file_path.startswith(root)

    remaining_path, end_of_path = split(file_path)
    path_components: list = [end_of_path]

    # While the remaining path is not the root directory or the root directory with a trailing slash
    while remaining_path != root and root != add_trailing_slash(dir_path=remaining_path):
        assert remaining_path != EMPTY_STRING

        remaining_path, end_of_path = split(remaining_path)
        path_components.insert(0, end_of_path)

    file_path: str = join(*path_components)
    return file_path

