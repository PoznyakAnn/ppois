from market import Market
from seller import Seller
from customer import Customer
from product import Product
from payment import Payment
from utils import is_valid_name, is_valid_product_name, save_state, load_state


def main():
    market = Market()

    load_choice = input("Хотите просмотреть данные с прошлого запуска? (да/нет): ").strip().lower()
    if load_choice == "да":
        try:
            market = load_state("market_state.pkl")
            print("Состояние рынка загружено.")
            market.show_sellers()
        except FileNotFoundError:
            print("Не удалось загрузить состояние, создается новый рынок.")


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

    while True:
        customer_name = input("Введите имя покупателя: ").strip()
        if is_valid_name(customer_name):
            break
        print("Ошибка: Имя покупателя должно содержать только буквы.")

    customer = Customer(customer_name)

    while True:
        print("\n1. Посмотреть продукты и скидки")
        print("2. Добавить продукт в корзину")
        print("3. Рассчитать общую стоимость")
        print("4. Поторговаться с продавцом")
        print("5. Посмотреть содержимое корзины")
        print("6. Оплатить корзину")
        print("7. Выйти")

        choice = input("Выберите опцию: ").strip()

        if choice == "1":
            current_day = input("Введите текущий день недели: ").strip().lower()
            valid_days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
            if current_day in valid_days:
                Customer.show_products(seller, current_day)
            else:
                print("Ошибка: неверный день недели. Пожалуйста, введите корректный день.")

        elif choice == "2":
            product_name = input("Введите название продукта для добавления в корзину: ").strip()
            product = next((p for p in seller.products if p.name.lower() == product_name.lower()), None)
            if product:
                customer.add_to_cart(product)
                print(f"{product.name} добавлено в корзину.")
            else:
                print("Ошибка: продукт не найден. Пожалуйста, проверьте правильность названия.")

        elif choice == "3":
            if customer.bargained:
                discounted_total = customer.calculate_discounted_total(seller.can_bargain())
                print(f"Общая стоимость {discounted_total:.2f} руб.")

            else:
                total_price = customer.calculate_total()
                print(f"Общая стоимость: {total_price:.2f} руб.")

        elif choice == "4":
            discounted_total = customer.calculate_discounted_total(seller.can_bargain())
            if seller.can_bargain():
                print(f"Общая стоимость после торга: {discounted_total:.2f} руб.")
                customer.bargained = True
            else:
                print(f"Общая стоимость: {discounted_total:.2f} руб. (торг невозможен)")

        elif choice == "5":
            customer.cart.show_cart(customer)

        elif choice == "6":
            Payment.handle_payment(seller)

        elif choice == "7":
            save_state(market, "market_state.pkl")
            print("Состояние рынка сохранено.")
            break

        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()