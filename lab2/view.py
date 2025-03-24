from PyQt6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem,
    QTreeWidget, QTreeWidgetItem, QPushButton,
    QMessageBox, QMenu, QDialog, QVBoxLayout, QWidget,
    QLabel, QHeaderView, QHBoxLayout
)
from PyQt6.QtCore import Qt
from dialogs import AddRecordDialog, SearchDeleteDialog


class TournamentView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Менеджер турниров")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()
        self.controller.load_data()  # Загружаем данные при старте

    def init_ui(self):
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Вид отображения (таблица/дерево)
        self.view_toggle = QPushButton("Показать дерево")
        self.view_toggle.clicked.connect(self.toggle_view)
        main_layout.addWidget(self.view_toggle)

        # Таблица для отображения данных
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Название турнира", "Дата проведения", "Вид спорта",
            "ФИО победителя", "Призовой фонд ($)", "Заработок победителя ($)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table)

        # Дерево для альтернативного отображения
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Параметр", "Значение"])
        self.tree.setColumnCount(2)
        self.tree.hide()
        main_layout.addWidget(self.tree)

        # Панель кнопок
        button_layout = QHBoxLayout()

        self.load_btn = QPushButton("Обновить данные")
        self.load_btn.clicked.connect(self.controller.load_data)
        button_layout.addWidget(self.load_btn)

        self.add_btn = QPushButton("Добавить запись")
        self.add_btn.clicked.connect(self.show_add_dialog)
        button_layout.addWidget(self.add_btn)

        self.search_delete_btn = QPushButton("Поиск/Удаление")
        self.search_delete_btn.clicked.connect(self.show_search_delete_menu)
        button_layout.addWidget(self.search_delete_btn)

        main_layout.addLayout(button_layout)

    def update_table(self, records):
        """Обновляет данные в таблице"""
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(record['Название турнира']))
            self.table.setItem(row, 1, QTableWidgetItem(record['Дата проведения']))
            self.table.setItem(row, 2, QTableWidgetItem(record['Вид спорта']))
            self.table.setItem(row, 3, QTableWidgetItem(record['ФИО победителя']))
            self.table.setItem(row, 4, QTableWidgetItem(f"{float(record['Призовой фонд']):,.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{float(record['Заработок победителя']):,.2f}"))

    def update_tree(self, records):
        """Обновляет данные в дереве"""
        self.tree.clear()
        for record in records:
            tournament_item = QTreeWidgetItem(self.tree)
            tournament_item.setText(0, record['Название турнира'])

            details = [
                ("Дата проведения", record['Дата проведения']),
                ("Вид спорта", record['Вид спорта']),
                ("Победитель", record['ФИО победителя']),
                ("Призовой фонд", f"{float(record['Призовой фонд']):,.2f} $"),
                ("Заработок победителя", f"{float(record['Заработок победителя']):,.2f} $")
            ]

            for param, value in details:
                item = QTreeWidgetItem(tournament_item)
                item.setText(0, param)
                item.setText(1, value)

    def toggle_view(self):
        """Переключает между таблицей и деревом"""
        if self.table.isVisible():
            self.table.hide()
            self.tree.show()
            self.view_toggle.setText("Показать таблицу")
        else:
            self.tree.hide()
            self.table.show()
            self.view_toggle.setText("Показать дерево")

    def show_add_dialog(self):
        """Показывает диалог добавления записи"""
        dialog = AddRecordDialog(self)
        if dialog.exec():
            self.controller.add_record_to_db(dialog.get_record())

    def show_search_delete_menu(self):
        """Показывает меню выбора поиска или удаления"""
        menu = QMenu(self)

        search_action = menu.addAction("🔍 Поиск записей")
        search_action.triggered.connect(self.show_search_dialog)

        delete_action = menu.addAction("🗑️ Удалить записи")
        delete_action.triggered.connect(self.show_delete_dialog)

        menu.exec(self.search_delete_btn.mapToGlobal(self.search_delete_btn.rect().bottomLeft()))

    def show_search_dialog(self):
        """Показывает диалог поиска с тремя типами критериев"""
        sports = self.controller.get_sports_list()
        dialog = SearchDeleteDialog(sports, is_delete_mode=False, parent=self)

        if dialog.exec():
            conditions = dialog.get_conditions()
            results = self.controller.search_records(conditions)
            self.show_search_results(results)

    def show_delete_dialog(self):
        """Показывает диалог удаления с тремя типами критериев"""
        sports = self.controller.get_sports_list()
        dialog = SearchDeleteDialog(sports, is_delete_mode=True, parent=self)

        if dialog.exec():
            confirm = QMessageBox.question(
                self,
                "Подтверждение удаления",
                "Вы уверены, что хотите удалить записи по выбранным критериям?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                deleted_count = self.controller.delete_records(dialog.get_conditions())
                QMessageBox.information(
                    self,
                    "Результат удаления",
                    f"Удалено записей: {deleted_count}",
                    QMessageBox.StandardButton.Ok
                )
                self.controller.load_data()

    def show_search_results(self, results):
        """Отображает результаты поиска в отдельном окне"""
        if not results:
            QMessageBox.information(self, "Результаты поиска", "Записи не найдены")
            return

        result_dialog = QDialog(self)
        result_dialog.setWindowTitle(f"Результаты поиска ({len(results)} записей)")
        result_dialog.resize(900, 500)

        layout = QVBoxLayout()

        # Таблица с результатами
        result_table = QTableWidget()
        result_table.setColumnCount(6)
        result_table.setHorizontalHeaderLabels([
            "Название турнира", "Дата проведения", "Вид спорта",
            "ФИО победителя", "Призовой фонд ($)", "Заработок победителя ($)"
        ])
        result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        result_table.setRowCount(len(results))
        for row, record in enumerate(results):
            result_table.setItem(row, 0, QTableWidgetItem(record['Название турнира']))
            result_table.setItem(row, 1, QTableWidgetItem(record['Дата проведения']))
            result_table.setItem(row, 2, QTableWidgetItem(record['Вид спорта']))
            result_table.setItem(row, 3, QTableWidgetItem(record['ФИО победителя']))
            result_table.setItem(row, 4, QTableWidgetItem(f"{float(record['Призовой фонд']):,.2f}"))
            result_table.setItem(row, 5, QTableWidgetItem(f"{float(record['Заработок победителя']):,.2f}"))

        layout.addWidget(result_table)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(result_dialog.accept)
        layout.addWidget(close_btn)

        result_dialog.setLayout(layout)
        result_dialog.exec()