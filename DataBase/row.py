from custom_types import PictureFile, RealInterval


class Row:
    def __init__(self, data):
        """
        Ініціалізація рядка таблиці.
        :param data: Дані рядка у вигляді словника.
        """
        self.data = data

    def to_dict(self):
        """
        Конвертація рядка у словник для збереження.
        :return: Словник із серіалізованими даними.
        """
        serialized_data = {}
        for key, value in self.data.items():
            if isinstance(value, PictureFile):
                serialized_data[key] = value.to_base64()
            elif isinstance(value, RealInterval):
                serialized_data[key] = value.to_dict()
            else:
                serialized_data[key] = value  # Базові типи
        return serialized_data

    @staticmethod
    def from_dict(data):
        """
        Створення рядка з словника.
        :param data: Словник із десеріалізованими даними.
        :return: Об'єкт Row.
        """
        deserialized_data = {}
        for key, value in data.items():
            if isinstance(value, str) and value.startswith("/9j/"):  # Base64 для картинки
                deserialized_data[key] = PictureFile.from_base64(value)
            elif isinstance(value, dict) and "start" in value and "end" in value:  # Інтервали
                deserialized_data[key] = RealInterval.from_dict(value)
            else:
                deserialized_data[key] = value  # Базові типи
        return Row(deserialized_data)
