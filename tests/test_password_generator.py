import unittest
import json
import string
import os
from password_generator import generate_password


class TestPasswordGenerator(unittest.TestCase):
    def test_password_length(self):
        password = generate_password(14, True, True, True)
        self.assertEqual(len(password), 14, "Длина пароля не соответствует ожидаемой")

    def test_password_uppercase(self):
        password = generate_password(14, True, True, True)
        self.assertTrue(any(c.isupper() for c in password), "В пароле отсутствуют заглавные буквы")

    def test_password_digits(self):
        password = generate_password(14, True, True, True)
        self.assertTrue(any(c.isdigit() for c in password), "В пароле отсутствуют цифры")

    def test_password_special_chars(self):
        special_chars = string.punctuation
        attempts = 10
        success = False
        for _ in range(attempts):
            password = generate_password(14, True, True, True)
            if any(c in special_chars for c in password):
                success = True
                break
        self.assertTrue(success, "Специальные символы отсутствуют в пароле после нескольких попыток")

    def test_json_storage(self):
        test_file = "test_passwords.json"
        passwords = [{"name": "test", "password": "test_password"}]
        with open(test_file, "w") as file:
            json.dump(passwords, file, indent=4)

        with open(test_file, "r") as file:
            loaded_passwords = json.load(file)

        self.assertEqual(passwords, loaded_passwords, "Пароли не совпадают после сохранения и загрузки")

        # удаляет тестовый файл после завершения теста
        os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
