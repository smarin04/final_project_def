from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Union

@dataclass
class Descriptor:
    data: List[Dict[str, Any]]

#noneRatio
    def none_ratio(self, columns: List[str] = "all"):
        if columns == "all":
            columns = list(self.data[0].keys())

        noneRatioResult = {}

        #Cols are Keys
        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")

            noneCount = 0
            #Rows are Values
            for row in self.data:
                if row[column] is None:
                    noneCount += 1
            noneRatioResult[column] = noneCount / len(self.data)

        return noneRatioResult

#avg
    def average(self, columns: List[str] = "all") -> Dict[str, float]:
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key],
                                                                        (int, float))]

        avgResult = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")
            elif not isinstance(self.data[0][column],
                                (int, float)):
                raise ValueError(f"Oops!  {column} was no valid NUMERIC column.  Try again...")

            values = [row[column] for row in self.data if row[column] is not None]
            avgResult[column] = sum(values) / len(values) if values else None

        return avgResult

#mdn
    def median(self, columns: List[str] = "all") -> Dict[str, float]:
        import statistics

        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key],
                                                                        (int, float))]

        mdnResult = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")
            elif not isinstance(self.data[0][column],
                                (int, float)):
                raise ValueError(f"Oops!  {column} was no valid NUMERIC column.  Try again...")

            values = [row[column] for row in self.data if row[column] is not None]
            mdnResult[column] = statistics.median(values) if values else None

        return mdnResult

#pctl
    def percentile(self, columns: List[str] = "all", percentile: int = 50) -> Dict[str, float]:
        import statistics

        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key],
                                                                        (int, float))]

        pctlResult = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")
            elif not isinstance(self.data[0][column],
                                (int, float)):
                raise ValueError(f"Oops!  {column} was no valid NUMERIC column.  Try again...")

            values = [row[column] for row in self.data if row[column] is not None]
            pctlResult[column] = statistics.quantiles(values, n=100, method="inclusive")[percentile-1] if values else None

        return pctlResult

#typeMode
    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str,
                                                                            Tuple[str,
                                                                                  Union[float, str, None]]]:
        import statistics

        if columns == "all":
            columns = list(self.data[0].keys())

        typeModeResult = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")



            values = [row[column] for row in self.data if row[column] is not None]
            if not values:
                #__name__
                typeModeResult[column] = (type(self.data[0][column]).__name__, None)
            elif isinstance(values[0], (int, float)):
                typeModeResult[column] = (type(values[0]).__name__, statistics.mode(values))
            else:
                typeModeResult[column] = (type(values[0]).__name__, statistics.mode(values))

        return typeModeResult



#NumPy
import numpy as np

@dataclass
class DescriptorNumpy:
    data: List[Dict[str, Any]]

#1
    def none_ratio(self, columns: List[str] = "all"):
        if columns == "all":
            columns = list(self.data[0].keys())

        noneRatioResultNp = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")

            #NumPy
            values = np.array([row[column] for row in self.data])
            noneCount = np.sum(values == None)
            noneRatioResultNp[column] = noneCount / len(self.data)

        return noneRatioResultNp

#2
    def average(self, columns: List[str] = "all") -> Dict[str, float]:
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key],
                                                                        (int, float))]

        avgResultNp = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")
            elif not isinstance(self.data[0][column],
                                (int, float)):
                raise ValueError(f"Oops!  {column} was no valid NUMERIC column.  Try again...")

            #NumPy
            values = np.array([row[column] for row in self.data if row[column] is not None])
            avgResultNp[column] = np.mean(values) if values.size > 0 else None

        return avgResultNp

#3
    def median(self, columns: List[str] = "all") -> Dict[str, float]:
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key],
                                                                        (int, float))]

        mdnResultNp = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")
            elif not isinstance(self.data[0][column],
                                (int, float)):
                raise ValueError(f"Oops!  {column} was no valid NUMERIC column.  Try again...")

            #NumPy
            values = np.array([row[column] for row in self.data if row[column] is not None])
            mdnResultNp[column] = np.median(values) if values.size > 0 else None

        return mdnResultNp

#4
    def percentile(self, columns: List[str] = "all", percentile: int = 50) -> Dict[str, float]:
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key],
                                                                        (int, float))]

        pctlResultNp = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")
            elif not isinstance(self.data[0][column],
                                (int, float)):
                raise ValueError(f"Oops!  {column} was no valid NUMERIC column.  Try again...")

            #NumPy
            values = np.array([row[column] for row in self.data if row[column] is not None])
            pctlResultNp[column] = np.percentile(values, percentile) if values.size > 0 else None

        return pctlResultNp

#5
    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str,
                                                                            Tuple[str,
                                                                                  Union[float, str, None]]]:
        if columns == "all":
            columns = list(self.data[0].keys())

        typeModeResultNp = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")

            #NumPy
            values = np.array([row[column] for row in self.data if row[column] is not None])
            if values.size == 0:
                typeModeResultNp[column] = (type(self.data[0][column]).__name__, None)
            elif np.issubdtype(values.dtype, np.number):
                typeModeResultNp[column] = (type(values[0]).__name__, float(np.bincount(values).argmax()))
            else:
                unique, counts = np.unique(values, return_counts=True)
                typeModeResultNp[column] = (type(values[0]).__name__, str(unique[np.argmax(counts)]))

        return typeModeResultNp
