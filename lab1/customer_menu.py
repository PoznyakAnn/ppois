from customer import Customer
from payment import Payment
from utils import is_valid_name


def customer_menu(market, seller):
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
                print(f"Барселона выиграла позавчера, так что продавец не прочь поторговаться, он согласился на скидку в 10%! Общая стоимость после торга: {discounted_total:.2f} руб.")
                customer.bargained = True
            else:
                print(f"Общая стоимость: {discounted_total:.2f} руб. (торг невозможен)")

        elif choice == "5":
            customer.cart.show_cart(customer)

        elif choice == "6":
            Payment.handle_payment(seller)

        elif choice == "7":
            break

        else:
            print("Неверный выбор. Попробуйте еще раз.")