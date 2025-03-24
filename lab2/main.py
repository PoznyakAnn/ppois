from PyQt6.QtWidgets import QApplication
from controller import TournamentController
from view import TournamentView
from model import TournamentModel
import sys


def main():
    app = QApplication(sys.argv)

    # Инициализация компонентов MVC
    model = TournamentModel()
    controller = TournamentController()
    view = TournamentView(controller)

    # Установка связей
    controller.model = model
    controller.view = view

    # Проверка и создание таблицы
    model.create_table_if_not_exists()

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()