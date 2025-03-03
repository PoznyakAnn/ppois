from product import Product
from cart import Cart
from seller import Seller

class Customer:
    def __init__(self, name: str) -> None:
        self.name = name
        self.cart = Cart()
        self.bargained = False

    def add_to_cart(self, product: Product):
        self.cart.add_product(product)

    def calculate_total(self):
        return self.cart.total_price()

    def calculate_discounted_total(self, can_bargain):

        if can_bargain:
            return self.cart.discounted_price(0.1)
        return self.calculate_total()

    @staticmethod
    def show_products(seller: Seller, day: str):
        print("Доступные продукты:")
        for product in seller.products:
            discount = seller.get_discount(day)
            if discount is not None:
                product.apply_discount(discount)
                print(f"{product.name} - {product.price:.2f} руб. (Скидка: {discount}%) - Цена со скидкой: {product.discounted_price:.2f} руб.")
            else:
                print(f"{product.name} - {product.price:.2f} руб.")