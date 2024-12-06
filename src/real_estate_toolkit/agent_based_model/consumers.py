from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional
from real_estate_toolkit.agent_based_model.houses import House, QualityScore                #!
from real_estate_toolkit.agent_based_model.house_market import HousingMarket                #!

class Segment(Enum):
    FANCY = auto()
    OPTIMIZER = auto()
    AVERAGE = auto()

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
        for year in range(years):
            self.savings += self.annual_income * self.saving_rate
            self.savings *= (1 + self.interest_rate)

        self.savings = round(self.savings, 2)

    def buy_a_house(self, housing_market: HousingMarket) -> None:
        suitableHouses = []

        if self.segment == Segment.FANCY:
            suitableHouses = [house for house in housing_market.houses
                               if house.is_new_construction()
                               and house.quality_score == QualityScore.EXCELLENT]
        elif self.segment == Segment.OPTIMIZER:
            monthly_income = self.annual_income / 12
            suitableHouses = [house for house in housing_market.houses
                               if house.calculate_price_per_square_foot() < monthly_income]
        elif self.segment == Segment.AVERAGE:
            avgPrice = housing_market.calculate_average_price()
            suitableHouses = [house for house in housing_market.houses
                               if house.price < avgPrice]

        for suitableHouse in suitableHouses:
            if self.savings >= suitableHouse.price:
                self.house = suitableHouse
                self.savings -= suitableHouse.price
                suitableHouse.sell_house()

                break
