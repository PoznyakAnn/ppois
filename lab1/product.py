class Product:
    def __init__(self, name: str, price: float, shelf_life: int) -> None:
        self.name = name
        self.price = price
        self.shelf_life = shelf_life
        self.discounted_price = price

    def apply_discount(self, discount: float):
        self.discounted_price = self.price * (1 - discount / 100)