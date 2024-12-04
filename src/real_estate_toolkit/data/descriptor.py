from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Union

@dataclass
class Descriptor:
    data: List[Dict[str, Any]]  #type hint



#3.1 noneRatio
    def none_ratio(self, columns: List[str] = "all"):   #default value, but "all" is not a List of str?
        if columns == "all":
            columns = list(self.data[0].keys())

        noneRatioResult = {}

        for column in columns:  #cols are keys
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")

            noneCount = 0
            for row in self.data:   #rows are values
                if row[column] is None:
                    noneCount += 1
            noneRatioResult[column] = noneCount / len(self.data)

        return noneRatioResult # type: ignore



#3.2 avg
    def average(self, columns: List[str] = "all") -> Dict[str, float]:
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key],
                                                                        (int, float))]   #no mg. complex?

        avgResult = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")
            elif not isinstance(self.data[0][column],
                                (int, float)):
                raise ValueError(f"Oops!  {column} was no valid NUMERIC column.  Try again...")

            values = [row[column] for row in self.data if row[column] is not None]  #no mg list comprehension.
            avgResult[column] = sum(values) / len(values) if values else None

        return avgResult # type: ignore



#3.3 mdn
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

        return mdnResult # type: ignore



#3.4 pctl
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
            pctlResult[column] = statistics.quantiles(values, n=100)[percentile-1] if values else None

        return pctlResult # type: ignore



#3.5 typeMode
    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str, Tuple[str, Union[float, str, None]]]:
        import statistics

        if columns == "all":
            columns = list(self.data[0].keys())

        typeModeResult = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")



            values = [row[column] for row in self.data if row[column] is not None]
            if not values:
                typeModeResult[column] = (type(self.data[0][column]).__name__, None)    #__name__
            elif isinstance(values[0], (int, float)):
                typeModeResult[column] = (type(values[0]).__name__, statistics.mode(values))
            else:
                typeModeResult[column] = (type(values[0]).__name__, statistics.mode(values))

        return typeModeResult # type: ignore







#4. NumPy
import numpy as np

@dataclass
class DescriptorNumpy:
    data: List[Dict[str, Any]]



#4.1
    def none_ratio(self, columns: List[str] = "all"):
        if columns == "all":
            columns = list(self.data[0].keys())

        noneRatioResult = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")

            #NumPy
            values = np.array([row[column] for row in self.data])
            noneCount = np.sum(values == None)
            noneRatioResult[column] = noneCount / len(self.data)

        return noneRatioResult # type: ignore



#4.2
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

            #NumPy
            values = np.array([row[column] for row in self.data if row[column] is not None])
            avgResult[column] = np.mean(values) if values.size > 0 else None

        return avgResult # type: ignore



#4.3
    def median(self, columns: List[str] = "all") -> Dict[str, float]:
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

            #NumPy
            values = np.array([row[column] for row in self.data if row[column] is not None])
            mdnResult[column] = np.median(values) if values.size > 0 else None

        return mdnResult # type: ignore



#4.4
    def percentile(self, columns: List[str] = "all", percentile: int = 50) -> Dict[str, float]:
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

            #NumPy
            values = np.array([row[column] for row in self.data if row[column] is not None])
            pctlResult[column] = np.percentile(values, percentile) if values.size > 0 else None

        return pctlResult # type: ignore



#4.5
    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str, Tuple[str, Union[float, str, None]]]:
        if columns == "all":
            columns = list(self.data[0].keys())

        typeModeResult = {}

        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Oops!  {column} was no valid column.  Try again...")

            #NumPy
            values = np.array([row[column] for row in self.data if row[column] is not None])
            if values.size == 0:
                typeModeResult[column] = (type(self.data[0][column]).__name__, None)
            elif np.issubdtype(values.dtype, np.number):
                typeModeResult[column] = (type(values[0]).__name__, float(np.bincount(values).argmax()))
            else:
                typeModeResult[column] = (type(values[0]).__name__, str(np.bincount(values).argmax()))

        return result # type: ignore
