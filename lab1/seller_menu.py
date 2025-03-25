from seller import Seller
from product import Product
from utils import is_valid_name, is_valid_product_name


def seller_menu(market):
    while True:
        seller_name = input("Введите имя продавца: ").strip()
        if is_valid_name(seller_name):
            break
        print("Ошибка: Имя продавца должно содержать только буквы.")

    seller = Seller(seller_name)

    while True:
        mood = input("Введите ваше настроение на текущий день (Хорошее/Плохое): ")
        if mood.lower() in ["хорошее", "плохое"]:
            seller.set_mood(mood)
            break
        print("Пожалуйста, введите 'Хорошее' или 'Плохое'.")

    market.add_seller(seller)

    while True:
        product_name = input("Введите название продукта (или 'выйти' для завершения): ").strip()
        if product_name.lower() == "выйти":
            break
        if not is_valid_product_name(product_name):
            print("Ошибка: Название продукта должно содержать только буквы, пробелы или дефисы.")
            continue

        while True:
            try:
                price = float(input(f"Введите цену для {product_name}: "))
                if price < 0:
                    raise ValueError("Цена не может быть отрицательной.")
                break
            except ValueError as e:
                print(f"Ошибка: {e}. Пожалуйста, введите корректное число для цены.")

        while True:
            try:
                shelf_life = int(input(f"Введите срок годности для {product_name} (в днях): "))
                if shelf_life < 0:
                    raise ValueError("Срок годности не может быть отрицательным.")
                break
            except ValueError as e:
                print(f"Ошибка: {e}. Пожалуйста, введите корректное число для срока годности.")

        product = Product(product_name, price, shelf_life)
        seller.add_product(product)

    while True:
        day = input("Введите день недели для установки скидки (или 'выйти' для завершения): ").strip().lower()
        if day == "выйти":
            break
        if day not in ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]:
            print("Ошибка: Пожалуйста, введите правильное название дня недели.")
            continue

        while True:
            try:
                discount = float(input(f"Введите скидку в процентах для {day}: "))
                if discount < 0:
                    raise ValueError("Скидка не может быть отрицательной.")
                seller.set_discount(day, discount)
                break
            except ValueError as e:
                print(f"Ошибка: {e}. Пожалуйста, введите корректное число для скидки.")

    return seller