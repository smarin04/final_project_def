from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class Cleaner:
    data: List[Dict[str, Any]]



#2.1.1
    def snake_case(self, name: str) -> str:
        import re   #re no mg demasiado
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        name = re.sub(r'\s+', '_', name)
        return name



#2.1
    def rename_with_best_practices(self) -> None:
        # if not self.data:
        #     return

        #data MUST be a list of dictionaries. FIRST dict is equivalent to DF.cols
        dataKeys = self.data[0].keys()
        dataKeysNew = {key: self.snake_case(key) for key in dataKeys}

        #renaming
        for row in self.data:
            for keyOld, keyNew in dataKeysNew.items():
                row[keyNew] = row.pop(keyOld)

        return self.data

#2.2
    def na_to_none(self) -> List[Dict[str, Any]]:
        for row in self.data:
            for key, value in row.items():
                if value == "NA":
                    row[key] = None

        return self.data
