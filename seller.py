from typing import List, Dict, Optional
from product import Product

class Seller:
    def __init__(self, name: str) -> None:
        self.name = name
        self.products: List[Product] = []
        self.discount_schedule: Dict[str, float] = {}
        self.mood: str = ""

    def add_product(self, product: Product):
        self.products.append(product)

    def set_discount(self, day: str, discount: float):
        self.discount_schedule[day] = discount

    def get_discount(self, day: str) -> Optional[float]:
        return self.discount_schedule.get(day)

    def set_mood(self, mood: str):
        self.mood = mood

    def can_bargain(self) -> bool:
        return self.mood.lower() == "хорошее"