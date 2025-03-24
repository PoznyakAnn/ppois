from PyQt6.QtWidgets import QMessageBox
from typing import List, Dict
class TournamentController:
    def __init__(self):
        self.model = None
        self.view = None

    def load_data(self) -> None:
        try:
            records = self.model.load_records_from_db()
            self.view.update_table(records)
            self.view.update_tree(records)
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка", f"Ошибка загрузки: {str(e)}")

    def add_record_to_db(self, record: Dict) -> bool:
        try:
            self.model.add_record(record)
            self.load_data()
            return True
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка", f"Ошибка добавления: {str(e)}")
            return False

    def delete_records(self, condition: str) -> int:
        try:
            deleted_count = self.model.delete_records(condition)
            self.load_data()
            return deleted_count
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка", f"Ошибка удаления: {str(e)}")
            return 0

    def search_records(self, conditions: str) -> List[Dict]:
        try:
            return self.model.search_records(conditions)
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка", f"Ошибка поиска: {str(e)}")
            return []

    def get_sports_list(self) -> List[str]:
        return self.model.get_sports_list()