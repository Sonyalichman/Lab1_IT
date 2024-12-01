import unittest
from custom_types import PictureFile, RealInterval

class TestCustomTypes(unittest.TestCase):

    def test_picture_file_base64(self):
        """Тест для збереження та відновлення зображення з Base64."""
        base64_data = "R0lGODdhAQABAIABAAAAAP///ywAAAAAAQABAAACAUwAOw=="  # 1x1 піксель
        picture = PictureFile(base64_data=base64_data)
        encoded = picture.to_base64()
        decoded_picture = PictureFile.from_base64(encoded)
        self.assertEqual(picture.data, decoded_picture.data)

    def test_real_interval_creation(self):
        """Тест для перевірки створення інтервалу."""
        interval = RealInterval(1.0, 5.0)
        self.assertEqual(interval.start, 1.0)
        self.assertEqual(interval.end, 5.0)

    def test_real_interval_to_dict(self):
        """Тест для перевірки серіалізації інтервалу."""
        interval = RealInterval(2.0, 6.0)
        interval_dict = interval.to_dict()
        self.assertEqual(interval_dict, {"start": 2.0, "end": 6.0})
        restored_interval = RealInterval.from_dict(interval_dict)
        self.assertEqual(restored_interval.start, 2.0)
        self.assertEqual(restored_interval.end, 6.0)

if __name__ == "__main__":
    unittest.main()
