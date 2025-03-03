
from market import Market

def is_valid_name(name: str) -> bool:
    return name.isalpha()

def is_valid_product_name(product_name: str) -> bool:

    return product_name.isalpha()

def save_state(market: Market, filename: str):
    market.save(filename)

def load_state(filename: str) -> Market:
    return Market.load(filename)