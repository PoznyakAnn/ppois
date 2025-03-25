from market import Market
from utils import save_state, load_state
from seller_menu import seller_menu
from customer_menu import customer_menu


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

    # Меню продавца
    seller = seller_menu(market)

    # Меню покупателя
    customer_menu(market, seller)

    save_state(market, "market_state.pkl")
    print("Состояние рынка сохранено.")


if __name__ == "__main__":
    main()