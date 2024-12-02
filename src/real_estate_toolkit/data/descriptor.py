from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union
import statistics

@dataclass
class Descriptor:
    """Class for summarizing and describing real estate data."""
    data: List[Dict[str, Any]]

    def none_ratio(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Compute the ratio of None value per column.
        If columns = "all" then compute for all.
        Validate that column names are correct. If not make an exception.
        Return a dictionary with the key as the variable name and value as the ratio.
        """
        if columns == "all":
            columns = list(self.data[0].keys())
        
        result = {}
        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Column {column} does not exist in the data.")
            none_count = sum(1 for row in self.data if row[column] is None)
            result[column] = none_count / len(self.data)
        return result # type: ignore
    
    def average(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Compute the average value for numeric variables. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the average
        """
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key], (int, float))]
        
        result = {}
        for column in columns:
            if column not in self.data[0] or not isinstance(self.data[0][column], (int, float)):
                raise ValueError(f"Column {column} is not a numeric variable.")
            values = [row[column] for row in self.data if row[column] is not None]
            result[column] = sum(values) / len(values) if values else None
        return result # type: ignore
    
    def median(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Compute the median value for numeric variables. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the median
        """
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key], (int, float))]
        
        result = {}
        for column in columns:
            if column not in self.data[0] or not isinstance(self.data[0][column], (int, float)):
                raise ValueError(f"Column {column} is not a numeric variable.")
            values = [row[column] for row in self.data if row[column] is not None]
            result[column] = statistics.median(values) if values else None
        return result # type: ignore
    
    def percentile(self, columns: Union[List[str], str] = "all", percentile: int = 50) -> Dict[str, float]:
        """Compute the percentile value for numeric variables. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the percentile
        """
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key], (int, float))]
        
        result = {}
        for column in columns:
            if column not in self.data[0] or not isinstance(self.data[0][column], (int, float)):
                raise ValueError(f"Column {column} is not a numeric variable.")
            values = [row[column] for row in self.data if row[column] is not None]
            result[column] = statistics.quantiles(values, n=100)[percentile-1] if values else None
        return result # type: ignore
    
    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str, Tuple[str, Union[float, str, None]]]:
        """Compute the mode for variables. Omit None values.
        If columns = "all" then compute for all.
        Validate that column names are correct. If not make an exception.
        Return a dictionary with the key as the variable name and value as a tuple of the variable type and the mode.
        If the variable is categorical
        """
        if columns == "all":
            columns = list(self.data[0].keys())
        
        result = {}
        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Column {column} does not exist in the data.")
            values = [row[column] for row in self.data if row[column] is not None]
            if not values:
                result[column] = (type(self.data[0][column]).__name__, None)
            elif isinstance(values[0], (int, float)):
                result[column] = (type(values[0]).__name__, statistics.mode(values))
            else:
                result[column] = (type(values[0]).__name__, statistics.mode(values))
        return result # type: ignore
    
    from dataclasses import dataclass
from typing import Any, Dict, List, Union
import numpy as np

@dataclass
class DescriptorNumpy:
    """Class for summarizing and describing real estate data using NumPy."""
    data: List[Dict[str, Any]]

    def none_ratio(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Compute the ratio of None value per column using NumPy.
        If columns = "all" then compute for all.
        Validate that column names are correct. If not make an exception.
        Return a dictionary with the key as the variable name and value as the ratio.
        """
        if columns == "all":
            columns = list(self.data[0].keys())
        
        result = {}
        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Column {column} does not exist in the data.")
            values = np.array([row[column] for row in self.data])
            none_count = np.sum(values == None)
            result[column] = none_count / len(self.data)
        return result # type: ignore
    
    def average(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Compute the average value for numeric variables using NumPy. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the average
        """
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key], (int, float))]
        
        result = {}
        for column in columns:
            if column not in self.data[0] or not isinstance(self.data[0][column], (int, float)):
                raise ValueError(f"Column {column} is not a numeric variable.")
            values = np.array([row[column] for row in self.data if row[column] is not None])
            result[column] = np.mean(values) if values.size > 0 else None
        return result # type: ignore
    
    def median(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Compute the median value for numeric variables using NumPy. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the median
        """
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key], (int, float))]
        
        result = {}
        for column in columns:
            if column not in self.data[0] or not isinstance(self.data[0][column], (int, float)):
                raise ValueError(f"Column {column} is not a numeric variable.")
            values = np.array([row[column] for row in self.data if row[column] is not None])
            result[column] = np.median(values) if values.size > 0 else None
        return result # type: ignore
    
    def percentile(self, columns: Union[List[str], str] = "all", percentile: int = 50) -> Dict[str, float]:
        """Compute the percentile value for numeric variables using NumPy. Omit None values.
        If columns = "all" then compute for all numeric ones.
        Validate that column names are correct and correspond to a numeric variable. If not make an exception.
        Return a dictionary with the key as the numeric variable name and value as the percentile
        """
        if columns == "all":
            columns = [key for key in self.data[0].keys() if isinstance(self.data[0][key], (int, float))]
        
        result = {}
        for column in columns:
            if column not in self.data[0] or not isinstance(self.data[0][column], (int, float)):
                raise ValueError(f"Column {column} is not a numeric variable.")
            values = np.array([row[column] for row in self.data if row[column] is not None])
            result[column] = np.percentile(values, percentile) if values.size > 0 else None
        return result # type: ignore
    
    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str, Union[Tuple[str, float], Tuple[str, str]]]:
        """Compute the mode for variables using NumPy. Omit None values.
        If columns = "all" then compute for all.
        Validate that column names are correct. If not make an exception.
        Return a dictionary with the key as the variable name and value as a tuple of the variable type and the mode.
        If the variable is categorical
        """
        if columns == "all":
            columns = list(self.data[0].keys())
        
        result = {}
        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Column {column} does not exist in the data.")
            values = np.array([row[column] for row in self.data if row[column] is not None])
            if values.size == 0:
                result[column] = (type(self.data[0][column]).__name__, None)
            elif np.issubdtype(values.dtype, np.number):
                result[column] = (type(values[0]).__name__, float(np.bincount(values).argmax()))
            else:
                result[column] = (type(values[0]).__name__, str(np.bincount(values).argmax()))
        return result # type: ignore