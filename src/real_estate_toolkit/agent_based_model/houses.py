from enum import Enum
from dataclasses import dataclass
from typing import Optional

class QualityScore(Enum):
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    FAIR = 2
    POOR = 1

@dataclass
class House:
    id: int
    price: float
    area: float
    bedrooms: int
    year_built: int
    quality_score: Optional[QualityScore]
    available: bool = True

#1
    def calculate_price_per_square_foot(self) -> float:
        if self.area == 0:
            pricePerSquareFoot = None
        else:
            pricePerSquareFoot = round(self.price / self.area, 2)
        return pricePerSquareFoot

#2
    from datetime import datetime
    def is_new_construction(self, current_year: int = datetime.now().year) -> bool:
        newConstruction = (current_year - self.year_built) < 5
        return newConstruction

#3
    def get_quality_score(self) -> None:
        from datetime import datetime

        if self.quality_score is None:
            age = datetime.now().year - self.year_built
            if age < 0 and self.area > 0 and self.bedrooms >= 0:
                self.quality_score = QualityScore.EXCELLENT
            elif age < 0 and self.area > 0 and self.bedrooms >= 0:
                self.quality_score = QualityScore.GOOD
            elif age < 0 and self.area > 0 and self.bedrooms >= 0:
                self.quality_score = QualityScore.AVERAGE
            elif age < 0 and self.area > 0 and self.bedrooms >= 0:
                self.quality_score = QualityScore.FAIR
            else:
                self.quality_score = QualityScore.POOR

#4
    def sell_house(self) -> None:
        self.available = False
