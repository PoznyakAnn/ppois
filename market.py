import pickle
from typing import List
from seller import Seller

class Market:
    def __init__(self):
        self.sellers: List[Seller] = []

    def add_seller(self, seller: Seller):
        self.sellers.append(seller)

    def save(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def show_sellers(self):
        if not self.sellers:
            print("Нет продавцов на рынке.")
        else:
            print("Продавцы на рынке:")
            for seller in self.sellers:
                print(f"Продавец: {seller.name}, Настроение: {seller.mood}")
                if seller.products:
                    print("Продукты:")
                    for product in seller.products:
                        print(f"- {product.name}, Цена: {product.price}, Срок годности: {product.shelf_life} дней")
                else:
                    print("Нет продуктов у продавца.")

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def view_saved_state(filename: str):

            try:
                with open(filename, 'rb') as file:
                    market = pickle.load(file)
                    print("Сохранённое состояние рынка:")
                    market.show_products()
            except FileNotFoundError:
                print("Не удалось найти файл для просмотра.")