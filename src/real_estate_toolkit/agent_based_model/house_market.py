from typing import List, Dict, Optional, Callable
from real_estate_toolkit.agent_based_model.houses import House, QualityScore      #!

from enum import Enum
class Segment(Enum):
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    FAIR = 2
    POOR = 1

class HousingMarket:
    def __init__(self,
                 houses: List[House]):
        self.houses: List[House] = houses

  #1
    def get_house_by_id(self,
                        house_id: int) -> House:
        for house in self.houses:
            if house.id == house_id:
                return house

        return (f"Oops!  {house_id} was no valid ID.  Try again...")

  #2
    def calculate_average_price(self,
                                bedrooms: Optional[int] = None) -> float:
        filteredHouses = [
            house for house in self.houses
            if bedrooms is None
            or house.bedrooms == bedrooms
            ]

        if not filteredHouses:
            return None

        totalPrice = sum(house.price for house in filteredHouses)
        avgPrice = totalPrice / len(filteredHouses)

        return avgPrice

  #3
    def get_houses_that_meet_requirements(self,
                                          max_price: int,
                                          segment: str) -> Optional[List[House]]:
        filteredHouses = [
            house for house in self.houses
            if house.price <= max_price
            and house.quality_score.value == segment.value
            ]                                                                     #!

        if not filteredHouses:
            return None

        return filteredHouses
