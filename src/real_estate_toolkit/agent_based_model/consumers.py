from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional
from .houses import House, QualityScore
from .house_market import HousingMarket

class Segment(Enum):
    FANCY = auto()  # House is new construction and house score is the highest
    OPTIMIZER = auto()  # Price per square foot is less than monthly salary
    AVERAGE = auto()  # House price is below the average housing market price

@dataclass
class Consumer:
    id: int
    annual_income: float
    children_number: int
    segment: Segment
    house: Optional[House] = None
    savings: float = 0.0
    saving_rate: float = 0.3
    interest_rate: float = 0.05
    
    def compute_savings(self, years: int) -> None:
        """
        Calculate accumulated savings over time.
        
        Implementation tips:
        - Use compound interest formula
        - Consider annual calculations
        - Account for saving_rate
        """
        for _ in range(years):
            self.savings += self.annual_income * self.saving_rate
            self.savings *= (1 + self.interest_rate)
    
    def buy_a_house(self, housing_market: HousingMarket) -> None:
        """
        Attempt to purchase a suitable house.
        
        Implementation tips:
        - Check savings against house prices
        - Consider down payment requirements
        - Match house to family size needs
        - Apply segment-specific preferences
        """
        suitable_houses = []
        
        if self.segment == Segment.FANCY:
            suitable_houses = [house for house in housing_market.houses if house.is_new_construction() and house.quality_score == QualityScore.EXCELLENT]
        elif self.segment == Segment.OPTIMIZER:
            monthly_salary = self.annual_income / 12
            suitable_houses = [house for house in housing_market.houses if house.calculate_price_per_square_foot() < monthly_salary]
        elif self.segment == Segment.AVERAGE:
            average_price = housing_market.calculate_average_price()
            suitable_houses = [house for house in housing_market.houses if house.price < average_price]
        
        for house in suitable_houses:
            if self.savings >= house.price:
                self.house = house
                self.savings -= house.price
                house.sell_house()
                break