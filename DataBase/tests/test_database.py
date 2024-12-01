import unittest
from database import Database
from schema import Schema, Field
from custom_types import RealInterval

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """
        Ініціалізація бази даних для тестів.
        """
        self.db = Database()
        fields = [
            Field("id", int),
            Field("name", str),
            Field("interval", RealInterval)
        ]
        self.schema = Schema(fields)
        self.db.create_table("TestTable", self.schema)

    def test_create_and_delete_table(self):
        """
        Тест для перевірки створення та видалення таблиці.
        """
        self.db.create_table("NewTable", self.schema)
        self.assertIn("NewTable", self.db.tables)
        self.db.delete_table("NewTable")
        self.assertNotIn("NewTable", self.db.tables)

    def test_save_and_load(self):
        """
        Тест для перевірки збереження та завантаження бази даних.
        """
        row_data = {"id": 1, "name": "Test", "interval": RealInterval(1.0, 5.0)}
        self.db.tables["TestTable"].add_row(row_data)
        self.db.save_to_disk("test_db.json")
        new_db = Database()
        new_db.load_from_disk("test_db.json")
        self.assertEqual(len(new_db.tables["TestTable"].rows), 1)

if __name__ == "__main__":
    unittest.main()
