from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any
import polars as pl

@dataclass
class DataLoader:
    data_path: Path

    def load_data_from_csv(self) -> List[Dict[str, Any]]:
        df = pl.read_csv(self.data_path, null_values="NA")
        dfToDicts = df.to_dicts()
        return dfToDicts

    def validate_columns(self, required_columns: List[str]) -> bool:
        df = pl.read_csv(self.data_path, null_values="NA")
        validateColumns = all(column in df.columns for column in required_columns)
        return validateColumns
