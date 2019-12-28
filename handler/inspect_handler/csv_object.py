"""Module containing the csv object class and the csv column classes that it depends on"""

from collections import Counter, Iterable
from numpy import isnan, issubdtype, ndarray, number
from pandas import DataFrame, read_csv, Series

from strings.general import CSV_EXTENSION, NAN
from strings.inspect_handler import INDENT, MAPPING_SYMBOL, MAX_KEY, MEAN_KEY, MIN_KEY, RANGE_KEY, STD_KEY


class CSVColumn:
    """Base class for objects containing useful information about csv columns"""

    N_INDENTS: int = 2

    def get_info(self) -> list:
        """Returns a list of strings containing information about the csv column"""

        raise NotImplementedError()


class CSVObject:
    """Contains necessary information about a csv file"""

    N_INDENTS: int = 1

    def __init__(self, csv_path: str):
        assert csv_path.endswith(CSV_EXTENSION)

        self._csv_cols: dict = {}

        df: DataFrame = read_csv(csv_path)
        for col_name in df.columns:
            self._csv_cols[col_name] = CSVObject._get_col(df=df, col_name=col_name)

    def get_csv_col_names(self) -> Iterable:
        """Returns the names of all the columns"""

        return self._csv_cols.keys()

    def get_nominal_cols(self) -> set:
        """
        Returns the csv columns that are nominal

        @return: The nominal column objects
        """

        nominal_cols: set = set()

        for csv_col in self._csv_cols.values():
            if type(csv_col) is NominalColumn:
                nominal_cols.add(csv_col)

        return nominal_cols

    def get_info(self) -> list:
        """Returns a list of strings containing useful information about the csv file corresponding to this object"""

        csv_obj_info: list = []

        # Sort the column names to ensure determinism
        col_names: list = sorted(self._csv_cols.keys())

        for col_name in col_names:
            col_name_line: str = (INDENT * CSVObject.N_INDENTS) + col_name
            csv_obj_info.append(col_name_line)

            col: CSVColumn = self._csv_cols[col_name]
            csv_col_info: list = col.get_info()
            csv_obj_info.extend(csv_col_info)
        return csv_obj_info

    @staticmethod
    def _get_col(df: DataFrame, col_name: str) -> CSVColumn:
        """
        Returns the csv column info object associated with a given data frame column

        @param df: The data frame that contains the column
        @param col_name: The name of the column
        @return: The csv column object
        """

        col: Series = df[col_name]

        if CSVObject._is_numeric(col=col):
            col: CSVColumn = NumericColumn(col=col)
            return col
        else:
            col: CSVColumn = NominalColumn(col=col)
            return col

    @staticmethod
    def _is_numeric(col: Series) -> bool:
        """
        Determines if a series contains only numerical values

        @param col: The series to check
        @return: The truth value of the above mentioned query
        """

        is_numeric: bool = issubdtype(col.dtype, number)
        return is_numeric


class NominalColumn(CSVColumn):
    """Contains useful information about csv columns with nominal values"""

    def __init__(self, col: Series):
        self._class_counts: Counter = Counter()

        # Get the frequency of each class in the nominal column
        for clazz in col:
            if type(clazz) is float:
                assert isnan(clazz)
                clazz: str = NAN
            self._class_counts[clazz] += 1

    def get_classes(self) -> Iterable:
        """
        Returns the classes of a nominal csv column

        @return: The collection of classes
        """

        return self._class_counts.keys()

    def get_info(self) -> list:
        """Returns a list of strings containing information about nominal csv columns"""

        csv_col_info: list = []

        # Sort the nominal column values to ensure determinism
        classes: list = sorted(self._class_counts.keys())

        for clazz in classes:
            class_count: int = self._class_counts[clazz]
            class_line: str = (INDENT * CSVColumn.N_INDENTS) + clazz + MAPPING_SYMBOL + str(class_count)
            csv_col_info.append(class_line)
        return csv_col_info


class NumericColumn(CSVColumn):
    """Contains useful information about csv columns with numeric values"""

    def __init__(self, col: Series):
        col: ndarray = col.to_numpy()

        self._min: number = col.min(initial=None)
        self._max: number = col.max(initial=None)
        self._range: number = self._max - self._min
        self._mean: number = col.mean()
        self._std: number = col.std()

    def get_info(self) -> list:
        """Returns a list of strings containing information about numeric csv columns"""

        csv_col_info: list = []
        NumericColumn._add_info_line(key=MIN_KEY, val=self._min, csv_col_info=csv_col_info)
        NumericColumn._add_info_line(key=MAX_KEY, val=self._max, csv_col_info=csv_col_info)
        NumericColumn._add_info_line(key=RANGE_KEY, val=self._range, csv_col_info=csv_col_info)
        NumericColumn._add_info_line(key=MEAN_KEY, val=self._mean, csv_col_info=csv_col_info)
        NumericColumn._add_info_line(key=STD_KEY, val=self._std, csv_col_info=csv_col_info)

        return csv_col_info

    @staticmethod
    def _add_info_line(key: str, val: number, csv_col_info: list):
        """
        Adds a line of numeric column information to a list

        @param key: The name of the data item
        @param val: The value of the data item
        @param csv_col_info: The list to add the information to
        """

        info_line: str = (INDENT * CSVColumn.N_INDENTS) + key + MAPPING_SYMBOL + str(val)
        csv_col_info.append(info_line)
