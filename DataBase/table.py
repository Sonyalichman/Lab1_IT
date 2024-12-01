from schema import Schema
from row import Row
from custom_types import PictureFile


class Table:
    def __init__(self, name, schema):
        """
        Ініціалізація таблиці з заданою схемою.
        :param name: Назва таблиці.
        :param schema: Об'єкт Schema.
        """
        self.name = name  # Назва таблиці
        self.schema = schema  # Об'єкт Schema
        self.rows = []  # Список рядків (Row)

    def add_row(self, data):
        """
        Додавання рядка до таблиці після валідації.
        :param data: Дані для додавання у рядок.
        """
        self.schema.validate(data)  # Перевірка відповідності схемі
        self.rows.append(Row(data))

    def edit_row(self, index, data):
        """
        Редагування рядка за індексом.
        :param index: Індекс рядка.
        :param data: Нові дані для рядка.
        """
        if index < 0 or index >= len(self.rows):
            raise IndexError("Індекс рядка поза межами.")
        self.schema.validate(data)  # Перевірка відповідності схемі
        self.rows[index] = Row(data)

    def delete_row(self, index):
        """
        Видалення рядка за індексом.
        :param index: Індекс рядка.
        """
        if index < 0 or index >= len(self.rows):
            raise IndexError("Індекс рядка поза межами.")
        del self.rows[index]

    def to_dict(self):
        """
        Конвертація таблиці у словник для збереження.
        :return: Словник із даними таблиці.
        """
        return {
            "name": self.name,
            "schema": self.schema.to_dict(),
            "rows": [row.to_dict() for row in self.rows]
        }

    def rename_or_reorder_columns(self, new_order):
        """
        Перейменування та/або перестановка колонок таблиці.
        :param new_order: Список нових назв колонок (у правильному порядку).
        """
        if len(new_order) != len(self.schema.fields):
            raise ValueError("Кількість нових назв колонок повинна співпадати з поточною.")

        # Перевіряємо, що всі поточні назви присутні в новому порядку
        current_names = [field.name for field in self.schema.fields]
        if sorted(current_names) != sorted(new_order):
            raise ValueError("Новий порядок повинен включати всі поточні назви колонок.")

        # Застосовуємо новий порядок колонок
        new_fields = []
        for new_name in new_order:
            for field in self.schema.fields:
                if field.name == new_name:
                    new_fields.append(field)
                    break
        self.schema.fields = new_fields

        # Переставляємо дані у рядках таблиці
        for row in self.rows:
            row.data = {new_name: row.data[new_name] for new_name in new_order}

    @staticmethod
    def from_dict(data):
        """
        Створення таблиці зі словника.
        :param data: Словник із даними таблиці.
        :return: Об'єкт Table.
        """
        schema = Schema.from_dict(data["schema"])
        table = Table(data["name"], schema)
        for row_data in data["rows"]:
            table.rows.append(Row.from_dict(row_data))
        return table
