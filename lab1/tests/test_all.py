import unittest
from product import Product
from seller import Seller
from customer import Customer
from cart import Cart



class TestProduct(unittest.TestCase):
    def test_product_creation(self):
        product = Product("Apple", 100.0, 10)
        expected_name = "Apple"
        expected_price = 100.0
        expected_shelf_life = 10

        self.assertEqual(product.name, expected_name)
        print(f"Ожидалось имя: {expected_name}, получено: {product.name}")

        self.assertEqual(product.price, expected_price)
        print(f"Ожидалась цена: {expected_price}, получена: {product.price}")

        self.assertEqual(product.shelf_life, expected_shelf_life)
        print(f"Ожидался срок годности: {expected_shelf_life}, получен: {product.shelf_life}")

    def test_apply_discount(self):
        product = Product("Apple", 100.0, 10)
        product.apply_discount(20)
        expected_discounted_price = 80.0

        self.assertEqual(product.discounted_price, expected_discounted_price)
        print(f"Ожидалась цена со скидкой: {expected_discounted_price}, получена: {product.discounted_price}")


class TestSeller(unittest.TestCase):
    def test_add_product(self):
        seller = Seller("John")
        product = Product("Apple", 100.0, 10)
        seller.add_product(product)

        self.assertIn(product, seller.products)
        print(f"Продукт {product.name} должен быть в списке продуктов продавца.")

    def test_set_discount(self):
        seller = Seller("John")
        seller.set_discount("понедельник", 20)
        expected_discount = 20

        self.assertEqual(seller.get_discount("понедельник"), expected_discount)
        print(f"Ожидалась скидка: {expected_discount}, получена: {seller.get_discount('понедельник')}")

    def test_can_bargain(self):
        seller = Seller("John")
        seller.set_mood("Хорошее")
        self.assertTrue(seller.can_bargain())
        print("Продавец должен уметь торговаться при хорошем настроении.")

        seller.set_mood("Плохое")
        self.assertFalse(seller.can_bargain())
        print("Продавец не должен уметь торговаться при плохом настроении.")


class TestCustomer(unittest.TestCase):
    def test_add_to_cart(self):
        customer = Customer("Alice")
        product = Product("Apple", 100.0, 10)
        customer.add_to_cart(product)

        self.assertIn(product, customer.cart.products)
        print(f"Продукт {product.name} должен быть в корзине покупателя.")

class TestPrices(unittest.TestCase):
    def test_add_to_cart(self):
        customer = Customer("Alice")
        product = Product("Apple", 100.0, 10)
        customer.add_to_cart(product)
        self.assertIn(product, customer.cart.products)

    def test_discount_day_with_bargain(self):
        seller = Seller("John")
        products = [
            Product("Apple", 100.0, 10),
            Product("Banana", 150.0, 5),
            Product("Orange", 200.0, 7)
        ]

        seller.set_discount("понедельник", 20)

        for product in products:
            product.apply_discount(seller.get_discount("понедельник"))

        customer = Customer("Alice")
        for product in products:
            customer.add_to_cart(product)

            # Проверяем общую стоимость в зависимости от возможности торга
        discounted_total = customer.calculate_discounted_total(seller.can_bargain())

        if seller.can_bargain():
            expected_total = (80 + 120 + 160) * 0.9  # Применяем 10% скидку
            self.assertEqual(discounted_total, expected_total)
            print(f"Ожидалась общая стоимость с торгом: {discounted_total}, получена {expected_total}")
        else:
            expected_total = 80 + 120 + 160  # Без торга
            self.assertEqual(discounted_total, expected_total)
            print(f"Ожидалась общая стоимость без торга: {discounted_total}, получена {expected_total}")


class TestCart(unittest.TestCase):
    def test_add_product(self):
        cart = Cart()
        product1 = Product("Apple", 100.0, 10)
        product2 = Product("Banana", 150.0, 5)
        cart.add_product(product1)
        cart.add_product(product2)

        self.assertIn(product1, cart.products)
        print(f"Продукт {product1.name} должен быть в корзине.")

        self.assertIn(product2, cart.products)
        print(f"Продукт {product2.name} должен быть в корзине.")




if __name__ == "__main__":
    unittest.main()