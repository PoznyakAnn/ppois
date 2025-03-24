from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QDateEdit,
    QLabel, QDoubleSpinBox, QMessageBox, QGroupBox,
    QRadioButton, QButtonGroup, QStackedWidget, QWidget
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QDoubleValidator


class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить запись")
        self.setFixedSize(400, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # Поля ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название турнира")

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setDisplayFormat("dd.MM.yyyy")
        self.date_input.setCalendarPopup(True)

        self.sport_combo = QComboBox()
        self.sport_combo.addItems(["Футбол", "Теннис", "Баскетбол", "Хоккей", "Шахматы"])

        self.winner_input = QLineEdit()
        self.winner_input.setPlaceholderText("Введите ФИО победителя")

        self.prize_input = QLineEdit()
        self.prize_input.setPlaceholderText("Введите сумму")
        self.prize_input.setValidator(QDoubleValidator(0, 10000000, 2))

        self.earnings_input = QLineEdit()
        self.earnings_input.setPlaceholderText("Рассчитывается автоматически")
        self.earnings_input.setReadOnly(True)

        # Привязка расчета заработка
        self.prize_input.textChanged.connect(self.calculate_earnings)

        # Добавление полей в форму
        form.addRow("Название турнира:", self.name_input)
        form.addRow("Дата проведения:", self.date_input)
        form.addRow("Вид спорта:", self.sport_combo)
        form.addRow("ФИО победителя:", self.winner_input)
        form.addRow("Призовой фонд ($):", self.prize_input)
        form.addRow("Заработок победителя ($):", self.earnings_input)

        layout.addLayout(form)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.validate_input)
        btn_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def calculate_earnings(self):
        """Рассчитывает заработок как 60% от призового фонда"""
        try:
            prize = float(self.prize_input.text())
            self.earnings_input.setText(f"{prize * 0.6:.2f}")
        except ValueError:
            self.earnings_input.clear()

    def validate_input(self):
        """Проверяет корректность ввода"""
        if not all([
            self.name_input.text(),
            self.winner_input.text(),
            self.prize_input.text()
        ]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return

        try:
            float(self.prize_input.text())
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Призовой фонд должен быть числом!")

    def get_record(self):
        """Возвращает данные в виде словаря"""
        return {
            'Название турнира': self.name_input.text(),
            'Дата проведения': self.date_input.date().toString("yyyy-MM-dd"),
            'Вид спорта': self.sport_combo.currentText(),
            'ФИО победителя': self.winner_input.text(),
            'Призовой фонд': self.prize_input.text(),
            'Заработок победителя': self.earnings_input.text()
        }


class SearchDeleteDialog(QDialog):
    def __init__(self, sports_list, is_delete_mode=False, parent=None):
        super().__init__(parent)
        self.sports_list = sports_list
        self.is_delete_mode = is_delete_mode
        self.setWindowTitle("Удаление записей" if is_delete_mode else "Поиск записей")
        self.setFixedSize(500, 450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Выбор типа критериев
        type_group = QGroupBox("Тип критериев")
        type_layout = QVBoxLayout()

        self.criteria_type = QButtonGroup()
        self.name_date_radio = QRadioButton("По названию/дате проведения")
        self.sport_winner_radio = QRadioButton("По виду спорта/победителю")
        self.prize_earnings_radio = QRadioButton("По призовому фонду/заработку")

        self.criteria_type.addButton(self.name_date_radio, 0)
        self.criteria_type.addButton(self.sport_winner_radio, 1)
        self.criteria_type.addButton(self.prize_earnings_radio, 2)

        type_layout.addWidget(self.name_date_radio)
        type_layout.addWidget(self.sport_winner_radio)
        type_layout.addWidget(self.prize_earnings_radio)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # StackedWidget для разных типов критериев
        self.stacked_widget = QStackedWidget()

        # 1. По названию или дате
        name_date_widget = QWidget()
        name_date_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название или часть")
        name_date_layout.addRow("Название турнира:", self.name_input)

        self.date_input = QDateEdit()
        self.date_input.setDisplayFormat("dd.MM.yyyy")
        self.date_input.setCalendarPopup(True)
        self.date_input.setSpecialValueText("Не выбрана")
        self.date_input.setDate(QDate())
        name_date_layout.addRow("Или дата проведения:", self.date_input)

        name_date_widget.setLayout(name_date_layout)
        self.stacked_widget.addWidget(name_date_widget)

        # 2. По виду спорта или победителю
        sport_winner_widget = QWidget()
        sport_winner_layout = QFormLayout()

        self.sport_combo = QComboBox()
        self.sport_combo.addItem("Не выбрано", None)
        self.sport_combo.addItems(self.sports_list)
        sport_winner_layout.addRow("Вид спорта:", self.sport_combo)

        self.winner_input = QLineEdit()
        self.winner_input.setPlaceholderText("Введите ФИО или часть имени")
        sport_winner_layout.addRow("Или победитель:", self.winner_input)

        sport_winner_widget.setLayout(sport_winner_layout)
        self.stacked_widget.addWidget(sport_winner_widget)

        # 3. По призовому фонду или заработку
        prize_earnings_widget = QWidget()
        prize_earnings_layout = QFormLayout()

        self.min_prize = QDoubleSpinBox()
        self.min_prize.setRange(0, 10000000)
        self.min_prize.setPrefix("От: ")
        self.min_prize.setSuffix(" $")
        prize_earnings_layout.addRow("Призовой фонд (мин):", self.min_prize)

        self.max_prize = QDoubleSpinBox()
        self.max_prize.setRange(0, 10000000)
        self.max_prize.setPrefix("До: ")
        self.max_prize.setSuffix(" $")
        prize_earnings_layout.addRow("Призовой фонд (макс):", self.max_prize)

        self.min_earnings = QDoubleSpinBox()
        self.min_earnings.setRange(0, 10000000)
        self.min_earnings.setPrefix("От: ")
        self.min_earnings.setSuffix(" $")
        prize_earnings_layout.addRow("Заработок (мин):", self.min_earnings)

        self.max_earnings = QDoubleSpinBox()
        self.max_earnings.setRange(0, 10000000)
        self.max_earnings.setPrefix("До: ")
        self.max_earnings.setSuffix(" $")
        prize_earnings_layout.addRow("Заработок (макс):", self.max_earnings)

        prize_earnings_widget.setLayout(prize_earnings_layout)
        self.stacked_widget.addWidget(prize_earnings_widget)

        layout.addWidget(self.stacked_widget)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.action_btn = QPushButton("Удалить" if self.is_delete_mode else "Найти")
        self.action_btn.clicked.connect(self.validate_input)
        btn_layout.addWidget(self.action_btn)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Связываем выбор типа с переключением страниц
        self.criteria_type.buttonClicked.connect(self.switch_criteria_type)
        self.name_date_radio.setChecked(True)

    def switch_criteria_type(self):
        self.stacked_widget.setCurrentIndex(self.criteria_type.checkedId())

    def validate_input(self):
        """Проверяет корректность ввода"""
        current_type = self.criteria_type.checkedId()

        if current_type == 0:  # Название/дата
            if not self.name_input.text() and not self.date_input.date().isValid():
                QMessageBox.warning(self, "Ошибка", "Укажите название или дату!")
                return

        elif current_type == 1:  # Спорт/победитель
            if self.sport_combo.currentData() is None and not self.winner_input.text():
                QMessageBox.warning(self, "Ошибка", "Укажите вид спорта или победителя!")
                return

        elif current_type == 2:  # Призовой/заработок
            if (self.min_prize.value() == 0 and self.max_prize.value() == 0 and
                    self.min_earnings.value() == 0 and self.max_earnings.value() == 0):
                QMessageBox.warning(self, "Ошибка", "Укажите хотя бы один диапазон!")
                return

        self.accept()

    def get_conditions(self):
        """Возвращает условия в формате SQL WHERE"""
        conditions = []
        current_type = self.criteria_type.checkedId()

        if current_type == 0:  # Название/дата
            if self.name_input.text():
                conditions.append(f"name LIKE '%{self.name_input.text().strip()}%'")
            if self.date_input.date().isValid():
                date = self.date_input.date().toString("yyyy-MM-dd")
                conditions.append(f"date = '{date}'")

        elif current_type == 1:  # Спорт/победитель
            if self.sport_combo.currentData():
                conditions.append(f"sport = '{self.sport_combo.currentData()}'")
            if self.winner_input.text():
                conditions.append(f"winner LIKE '%{self.winner_input.text().strip()}%'")

        elif current_type == 2:  # Призовой/заработок
            if self.min_prize.value() > 0 or self.max_prize.value() > 0:
                min_p = self.min_prize.value()
                max_p = self.max_prize.value() if self.max_prize.value() > 0 else 9999999
                conditions.append(f"prize BETWEEN {min_p} AND {max_p}")
            if self.min_earnings.value() > 0 or self.max_earnings.value() > 0:
                min_e = self.min_earnings.value()
                max_e = self.max_earnings.value() if self.max_earnings.value() > 0 else 9999999
                conditions.append(f"earnings BETWEEN {min_e} AND {max_e}")

        return " AND ".join(conditions) if conditions else "1=0"