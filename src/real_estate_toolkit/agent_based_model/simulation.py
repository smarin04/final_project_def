from enum import Enum, auto
from dataclasses import dataclass
from random import gauss, randint, choice
from typing import List, Dict, Any, Optional
from .houses import House, QualityScore
from .house_market import HousingMarket
from .consumers import Segment, Consumer

class CleaningMarketMechanism(Enum):
    INCOME_ORDER_DESCENDANT = auto()
    INCOME_ORDER_ASCENDANT = auto()
    RANDOM = auto()

@dataclass
class AnnualIncomeStatistics:
    minimum: float
    average: float
    standard_deviation: float
    maximum: float

@dataclass
class ChildrenRange:
    minimum: float = 0
    maximum: float = 5

@dataclass
class Simulation:
    housing_market_data: List[Dict[str, Any]]
    consumers_number: int
    years: int
    annual_income: AnnualIncomeStatistics
    children_range: ChildrenRange
    cleaning_market_mechanism: CleaningMarketMechanism
    down_payment_percentage: float = 0.2
    saving_rate: float = 0.3
    interest_rate: float = 0.05

    def __post_init__(self):
        self.housing_market: Optional[HousingMarket] = None
        self.consumers: List[Consumer] = []

    def create_housing_market(self):
            houses = []
            for data in self.housing_market_data:
                quality_score = QualityScore(max(1, min(5, int(data["overall_qual"]) // 2)))
                house = House(
                    id=int(data["id"]),
                    price=float(data["sale_price"]),
                    area=float(data["gr_liv_area"]),
                    bedrooms=int(data["bedroom_abv_gr"]),
                    year_built=int(data["year_built"]),
                    quality_score=quality_score,
                    available=True
                )
                houses.append(house)
            self.housing_market = HousingMarket(houses)

    def create_consumers(self) -> None:
        for i in range(self.consumers_number):
            while True:
                annual_income = gauss(self.annual_income.average, self.annual_income.standard_deviation)
                if self.annual_income.minimum <= annual_income <= self.annual_income.maximum:
                    break

            children_number = randint(self.children_range.minimum, self.children_range.maximum)
            segment = choice(list(Segment))
            consumer = Consumer(
                id=i,
                annual_income=annual_income,
                children_number=children_number,
                segment=segment,
                saving_rate=self.saving_rate,
                interest_rate=self.interest_rate
            )
            self.consumers.append(consumer)

    def compute_consumers_savings(self) -> None:
        for consumer in self.consumers:
            consumer.savings += consumer.annual_income * consumer.saving_rate

    def clean_the_market(self) -> None:
        if self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_DESCENDANT:
            self.consumers.sort(key=lambda c: c.annual_income, reverse=True)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_ASCENDANT:
            self.consumers.sort(key=lambda c: c.annual_income)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.RANDOM:
            from random import shuffle
            shuffle(self.consumers)

        for consumer in self.consumers:
            for house in self.housing_market.houses:
                if house.available and consumer.savings >= self.down_payment_percentage * house.price:
                    consumer.house = house
                    house.available = False
                    break

    def compute_owners_population_rate(self) -> float:
        owners = sum(1 for consumer in self.consumers if consumer.house is not None)
        return owners / len(self.consumers) if self.consumers else 0

    def compute_houses_availability_rate(self) -> float:
        available_houses = sum(1 for house in self.housing_market.houses if house.available)
        total_houses = len(self.housing_market.houses)
        return available_houses / total_houses if total_houses else 0
