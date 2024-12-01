import json
from table import Table


class Database:
    def __init__(self):
        """
        Ініціалізація бази даних.
        """
        self.tables = {}  # Словник для зберігання таблиць

    def create_table(self, name, schema):
        """
        Створення таблиці з заданим іменем та схемою.
        :param name: Назва таблиці.
        :param schema: Схема таблиці.
        """
        if name in self.tables:
            raise ValueError(f"Таблиця з іменем '{name}' вже існує.")
        self.tables[name] = Table(name, schema)

    def delete_table(self, name):
        """
        Видалення таблиці за іменем.
        :param name: Назва таблиці.
        """
        if name not in self.tables:
            raise ValueError(f"Таблиця з іменем '{name}' не знайдена.")
        del self.tables[name]

    def save_to_disk(self, filename):
        """
        Збереження бази даних на диск.
        :param filename: Назва файлу для збереження.
        """
        data = {name: table.to_dict() for name, table in self.tables.items()}
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_from_disk(self, filename):
        """
        Завантаження бази даних з диска.
        :param filename: Назва файлу для завантаження.
        """
        with open(filename, 'r') as file:
            data = json.load(file)
            for name, table_data in data.items():
                self.tables[name] = Table.from_dict(table_data)
