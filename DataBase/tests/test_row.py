import unittest
from row import Row
from custom_types import RealInterval

class TestRow(unittest.TestCase):

    def test_row_serialization(self):
        """
        Тест для перевірки серіалізації та десеріалізації рядка.
        """
        data = {"id": 1, "name": "Test", "interval": RealInterval(0.0, 10.0)}
        row = Row(data)
        serialized = row.to_dict()
        deserialized_row = Row.from_dict(serialized)

        # Порівнюємо значення всередині словника
        self.assertEqual(row.data["id"], deserialized_row.data["id"])
        self.assertEqual(row.data["name"], deserialized_row.data["name"])
        self.assertEqual(row.data["interval"].start, deserialized_row.data["interval"].start)
        self.assertEqual(row.data["interval"].end, deserialized_row.data["interval"].end)

    def test_row_data_access(self):
        """
        Тест для перевірки доступу до даних рядка.
        """
        data = {"id": 123, "value": "Example"}
        row = Row(data)
        self.assertEqual(row.data["id"], 123)
        self.assertEqual(row.data["value"], "Example")

if __name__ == "__main__":
    unittest.main()
