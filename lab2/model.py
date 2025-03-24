import sqlite3
from typing import List, Dict


class TournamentModel:
    def __init__(self):
        self.db_name = "tournaments.db"
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                sport TEXT NOT NULL,
                winner TEXT NOT NULL,
                prize REAL NOT NULL,
                earnings REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def load_records_from_db(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name, date, sport, winner, prize, earnings FROM tournaments")
        records = cursor.fetchall()
        conn.close()

        return [{
            'Название турнира': r[0],
            'Дата проведения': r[1],
            'Вид спорта': r[2],
            'ФИО победителя': r[3],
            'Призовой фонд': float(r[4]),
            'Заработок победителя': float(r[5])
        } for r in records]

    def add_record(self, record: Dict) -> None:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tournaments (name, date, sport, winner, prize, earnings) VALUES (?, ?, ?, ?, ?, ?)",
            (
                record['Название турнира'],
                record['Дата проведения'],
                record['Вид спорта'],
                record['ФИО победителя'],
                float(record['Призовой фонд']),
                float(record['Заработок победителя'])
            )
        )
        conn.commit()
        conn.close()

    def delete_records(self, condition: str) -> int:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM tournaments WHERE {condition}")
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
        except sqlite3.Error as e:
            raise Exception(f"Ошибка при удалении: {str(e)}")
        finally:
            conn.close()

    def search_records(self, conditions: str) -> List[Dict]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            query = f"SELECT name, date, sport, winner, prize, earnings FROM tournaments WHERE {conditions}"
            cursor.execute(query)
            records = cursor.fetchall()

            return [{
                'Название турнира': r[0],
                'Дата проведения': r[1],
                'Вид спорта': r[2],
                'ФИО победителя': r[3],
                'Призовой фонд': float(r[4]),
                'Заработок победителя': float(r[5])
            } for r in records]
        except sqlite3.Error as e:
            raise Exception(f"Ошибка при поиске: {str(e)}")
        finally:
            conn.close()

    def get_sports_list(self) -> List[str]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT sport FROM tournaments")
        sports = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sorted(sports)