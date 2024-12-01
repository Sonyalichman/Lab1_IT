import base64

class PictureFile:
    def __init__(self, filepath=None, base64_data=None):
        """
        Ініціалізація об'єкта з файлу або з base64-даних.
        :param filepath: Шлях до файлу зображення.
        :param base64_data: Дані у форматі base64.
        """
        if filepath:
            with open(filepath, 'rb') as file:
                self.data = file.read()
        elif base64_data:
            self.data = base64.b64decode(base64_data)
        else:
            raise ValueError("Необхідно вказати або 'filepath', або 'base64_data'.")

    def to_base64(self):
        """
        Перетворює дані зображення у формат base64.
        :return: Строка у форматі base64.
        """
        return base64.b64encode(self.data).decode('utf-8')

    @staticmethod
    def from_base64(base64_data):
        """
        Створює об'єкт PictureFile з base64-даних.
        :param base64_data: Дані у форматі base64.
        :return: Об'єкт PictureFile.
        """
        return PictureFile(base64_data=base64_data)

    def save_to_file(self, filepath):
        """
        Зберігає зображення у файл.
        :param filepath: Шлях до файлу, де потрібно зберегти зображення.
        """
        with open(filepath, 'wb') as file:
            file.write(self.data)

    def __repr__(self):
        """
        Представлення об'єкта як тексту.
        :return: Повідомлення про збереження зображення.
        """
        return "Зображення збережено"

class RealInterval:
    def __init__(self, start, end):
        """
        Ініціалізація інтервалу дійсних чисел.
        :param start: Початок інтервалу.
        :param end: Кінець інтервалу.
        """
        self.start = float(start)
        self.end = float(end)

    def to_dict(self):
        """
        Перетворює інтервал у словник.
        :return: Словник з ключами 'start' і 'end'.
        """
        return {"start": self.start, "end": self.end}

    @staticmethod
    def from_dict(data):
        """
        Створює об'єкт RealInterval зі словника.
        :param data: Словник з ключами 'start' і 'end'.
        :return: Об'єкт RealInterval.
        """
        return RealInterval(data["start"], data["end"])

    def __repr__(self):
        """
        Представлення об'єкта як тексту.
        :return: Текстове представлення інтервалу.
        """
        return f"{self.start} - {self.end}"
