from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class Cleaner:
    data: List[Dict[str, Any]]

    def snake_case(self, colName: str) -> str:
        import re
        colName = re.sub(r"(?<!^)(?=[A-Z])", "_", colName).lower()
        return colName

    def rename_with_best_practices(self) -> None:
        dataKeys = self.data[0].keys()

        #New Data Keys
        dataKeysNew = {key: self.snake_case(key) for key in dataKeys}

        #Rename
        for row in self.data:
            for keyOld, keyNew in dataKeysNew.items():
                row[keyNew] = row.pop(keyOld)

        return self.data

    def na_to_none(self) -> List[Dict[str, Any]]:
        for row in self.data:
            for key, value in row.items():
                if value == "NA":
                    row[key] = None

        return self.data
