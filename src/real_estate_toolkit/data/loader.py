from dataclasses import dataclass
from pathlib import Path    #type hint
from typing import Dict, List, Any  #more type hints. Union[int, str]
import polars as pl

@dataclass  #decorator
class DataLoader:
    data_path: Path

    def load_data_from_csv(self) -> List[Dict[str, Any]]:
        df = pl.read_csv(self.data_path)
        dfToDicts = df.to_dicts()
        return dfToDicts

    def validate_columns(self, required_columns: List[str]) -> bool:
        df = pl.read_csv(self.data_path)
        validateColumns = all(column in df.columns for column in required_columns)
        return validateColumns
