import unittest
from table import Table
from schema import Schema, Field
from custom_types import RealInterval

class TestTable(unittest.TestCase):

    def setUp(self):
        """
        Ініціалізація таблиці для тестів.
        """
        self.fields = [
            Field("id", int),
            Field("name", str),
            Field("interval", RealInterval)
        ]
        self.schema = Schema(self.fields)
        self.table = Table("TestTable", self.schema)

    def test_add_row(self):
        """
        Тест для перевірки додавання рядка.
        """
        row_data = {"id": 1, "name": "Test", "interval": RealInterval(1.0, 5.0)}
        self.table.add_row(row_data)
        self.assertEqual(len(self.table.rows), 1)

    def test_reorder_columns(self):
        """
        Тест для перевірки перестановки колонок.
        """
        row_data = {"id": 1, "name": "Test", "interval": RealInterval(1.0, 5.0)}
        self.table.add_row(row_data)
        self.table.rename_or_reorder_columns(["name", "interval", "id"])
        self.assertEqual(list(self.table.rows[0].data.keys()), ["name", "interval", "id"])

if __name__ == "__main__":
    unittest.main()
