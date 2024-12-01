from custom_types import PictureFile
from custom_types import RealInterval

class Field:
    def __init__(self, name, data_type):
        """
        Ініціалізація поля таблиці.
        :param name: Назва поля.
        :param data_type: Тип даних поля.
        """
        self.name = name  # Назва поля
        self.data_type = data_type  # Тип даних поля

    def validate(self, value):
        """
        Валідація значення поля.
        :param value: Значення, яке потрібно перевірити.
        :return: True, якщо значення валідне, інакше False.
        """
        if self.data_type == "picture":
            return isinstance(value, PictureFile)
        elif self.data_type == "realInvl":
            return isinstance(value, RealInterval)
        elif self.data_type == "char":
            return isinstance(value, str) and len(value) == 1
        else:
            return isinstance(value, self.data_type)

    def to_dict(self):
        """
        Конвертація поля у словник для збереження.
        :return: Словник із параметрами поля.
        """
        valid_types = {
            int: "int",
            float: "float",
            str: "str",
            "char": "char",
            PictureFile: "picture",
            RealInterval: "realInvl"
        }
        data_type_str = valid_types.get(self.data_type, str(self.data_type))
        return {
            "name": self.name,
            "data_type": data_type_str
        }

    @staticmethod
    def from_dict(data):
        """
        Створення поля з словника.
        :param data: Словник із параметрами поля.
        :return: Об'єкт Field.
        """
        print(f"Відновлення поля: {data}")  # Відладочний друк
        valid_types = {
            "int": int,
            "float": float,
            "str": str,
            "char": "char",
            "picture": PictureFile,
            "realInvl": RealInterval
        }
        field_type = valid_types.get(data["data_type"])
        if not field_type:
            raise ValueError(f"Невідомий тип даних: {data['data_type']}")
        return Field(data["name"], field_type)


class Schema:
    def __init__(self, fields):
        """
        Ініціалізація схеми таблиці.
        :param fields: Список об'єктів Field.
        """
        self.fields = fields  # Список об'єктів Field

    def validate(self, data):
        """
        Перевірка, чи відповідають дані схемі.
        :param data: Дані для перевірки.
        :raises ValueError: Якщо в даних відсутнє поле.
        :raises TypeError: Якщо тип даних не відповідає схемі.
        """
        for field in self.fields:
            if field.name not in data:
                raise ValueError(f"Поле '{field.name}' відсутнє у даних.")
            if not field.validate(data[field.name]):
                raise TypeError(f"Поле '{field.name}' повинно бути типу {field.data_type}.")

    def has_field(self, field_name):
        """
        Перевірка наявності поля у схемі.
        :param field_name: Назва поля.
        :return: True, якщо поле є у схемі.
        """
        return any(field.name == field_name for field in self.fields)

    def to_dict(self):
        """
        Конвертація схеми у словник для збереження.
        :return: Словник із параметрами схеми.
        """
        return {
            "fields": [field.to_dict() for field in self.fields]
        }

    @staticmethod
    def from_dict(data):
        """
        Створення схеми з словника.
        :param data: Словник із параметрами схеми.
        :return: Об'єкт Schema.
        """
        fields = [Field.from_dict(field_data) for field_data in data["fields"]]
        return Schema(fields)
