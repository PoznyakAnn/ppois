import time
from customer import Customer
from seller import Seller

class Payment:
    def __init__(self):
        pass

    @staticmethod
    def handle_payment(seller: Seller) -> None:
        payment_method = input("Выберите способ оплаты (карта/нал): ").strip().lower()

        if payment_method == "карта":
            print("Производится оплата...")
            time.sleep(2)
            print(f"{seller.name}: Оплата прошла. Спасибо, приходите еще!")
        elif payment_method == "нал":
            print("Передача денег...")
            time.sleep(2)
            print(f"{seller.name}: Спасибо, приходите еще!")
        else:
            print("Ошибка: Неверный способ оплаты. Пожалуйста, выберите 'карта' или 'нал'.")


