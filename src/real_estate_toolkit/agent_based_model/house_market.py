from typing import List, Optional, Dict, Callable
from real_estate_toolkit.agent_based_model.houses import House, QualityScore

class HousingMarket:
    def __init__(self, houses: List[House]):
        self.houses: List[House] = houses
    
    def get_house_by_id(self, house_id: int) -> Optional[House]:
        """
        Retrieve specific house by ID.
        
        Implementation tips:
        - Use efficient search method
        - Handle non-existent IDs
        """
        for house in self.houses:
            if house.id == house_id:
                return house
        return None
    
    def calculate_average_price(self, bedrooms: Optional[int] = None) -> float:
        """
        Calculate average house price, optionally filtered by bedrooms.
        
        Implementation tips:
        - Handle empty lists
        - Consider using statistics module
        - Implement bedroom filtering efficiently
        """
        filtered_houses = [house for house in self.houses if bedrooms is None or house.bedrooms == bedrooms]
        if not filtered_houses:
            return 0.0
        total_price = sum(house.price for house in filtered_houses)
        return total_price / len(filtered_houses)
    
    def get_houses_that_meet_requirements(self, max_price: float, segment: str) -> Optional[List[House]]:
        """
        Filter houses based on buyer requirements.
        
        Implementation tips:
        - Consider multiple filtering criteria
        - Implement efficient filtering
        - Handle case when no houses match
        """
        segment_criteria: Dict[str, Callable[[House], bool]] = {
            "luxury": lambda house: house.quality_score == QualityScore.EXCELLENT,
            "premium": lambda house: house.quality_score in {QualityScore.EXCELLENT, QualityScore.GOOD},
            "standard": lambda house: house.quality_score in {QualityScore.EXCELLENT, QualityScore.GOOD, QualityScore.AVERAGE},
            "budget": lambda house: house.quality_score in {QualityScore.FAIR, QualityScore.POOR}
        }
        
        if segment not in segment_criteria:
            return None
        
        filtered_houses = [house for house in self.houses if house.price <= max_price and segment_criteria[segment](house)]
        return filtered_houses if filtered_houses else None