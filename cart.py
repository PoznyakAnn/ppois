
class Cart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def total_price(self):
        return sum(product.discounted_price for product in self.products)

    def discounted_price(self, discount_rate):
        total = self.total_price()
        return total * (1 - discount_rate)

    def show_cart(self, customer):
        if not self.products:
            print("Корзина пуста.")
            return

        print("Содержимое корзины:")
        total_price = 0

        for product in self.products:
            if customer.bargained:
                discounted_price = product.discounted_price * 0.9
                print(f"{product.name}: {discounted_price:.2f} руб. (после торга: {product.price:.2f} руб.)")
                total_price += discounted_price
            else:
                print(
                    f"{product.name}: {product.discounted_price:.2f} руб. (оригинальная цена: {product.price:.2f} руб.)")
                total_price += product.discounted_price