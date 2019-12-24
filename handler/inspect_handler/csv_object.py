"""Module containing the csv object class and the csv column class that it depends on"""

from pandas import DataFrame, read_csv, Series

from strings.general import CSV_EXTENSION


class CSVObject:
    """Contains necessary information about a csv file"""

    def __init__(self, csv_path: str):
        assert csv_path.endswith(CSV_EXTENSION)

        self._csv_cols: dict = {}

        df: DataFrame = read_csv(csv_path)
        # TODO: Iterate through each column and fill the list of csv columns


class NominalColumn:
    """A csv column with nominal values"""

    def __init__(self, col: Series):
        # TODO
        pass


class NumericColumn:
    """A csv column with numeric values"""

    def __init__(self, col: Series):
        # TODO
        pass
