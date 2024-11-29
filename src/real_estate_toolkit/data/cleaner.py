from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class Cleaner:
    """Class for cleaning real estate data."""
    data: List[Dict[str, Any]]
    
    def rename_with_best_practices(self) -> None:
        """Rename the columns with best practices (e.g. snake_case very descriptive name)."""
        if not self.data:
            return
        
        # Get the keys from the first dictionary to rename columns
        original_keys = self.data[0].keys()
        new_keys = {key: self._to_snake_case(key) for key in original_keys}
        
        # Rename columns in each dictionary
        for row in self.data:
            for old_key, new_key in new_keys.items():
                row[new_key] = row.pop(old_key)
    
    def na_to_none(self) -> List[Dict[str, Any]]:
        """Replace NA to None in all values with NA in the dictionary."""
        for row in self.data:
            for key, value in row.items():
                if value == "NA":
                    row[key] = None
        return self.data
    
    def _to_snake_case(self, name: str) -> str:
        """Convert a string to snake_case."""
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        name = re.sub(r'\s+', '_', name)
        return name