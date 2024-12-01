import unittest
from schema import Schema, Field
from custom_types import RealInterval

class TestSchema(unittest.TestCase):

    def setUp(self):
        """
        Ініціалізація схеми для тестів.
        """
        self.fields = [
            Field("id", int),
            Field("name", str),
            Field("interval", RealInterval)
        ]
        self.schema = Schema(self.fields)

    def test_schema_validation(self):
        """
        Тест для перевірки валідації даних за схемою.
        """
        valid_data = {"id": 1, "name": "Test", "interval": RealInterval(1.0, 5.0)}
        self.schema.validate(valid_data)
        invalid_data = {"id": "not_an_int", "name": "Test", "interval": RealInterval(1.0, 5.0)}
        with self.assertRaises(TypeError):
            self.schema.validate(invalid_data)

    def test_schema_serialization(self):
        """
        Тест для перевірки серіалізації схеми.
        """
        serialized = self.schema.to_dict()
        deserialized_schema = Schema.from_dict(serialized)
        self.assertEqual(len(deserialized_schema.fields), len(self.schema.fields))

if __name__ == "__main__":
    unittest.main()
