import unittest
import json
import os
from password_generator import generate_password


class TestAppLogic(unittest.TestCase):
    def test_save_and_load_passwords(self):
        # проверка сохранения и загрузки паролей
        test_file = "test_passwords.json"
        passwords = [{"name": "test1", "password": "password123"}, {"name": "test2", "password": "anotherpassword"}]

        # сохранение паролей в файл
        with open(test_file, "w") as file:
            json.dump(passwords, file, indent=4)

        # загрузка паролей из файла
        with open(test_file, "r") as file:
            loaded_passwords = json.load(file)

        # проверка соответствия сохраненных и загруженных данных
        self.assertEqual(passwords, loaded_passwords, "Сохраненные и загруженные пароли не совпадают")

        # удаление тестового файла после завершения теста
        os.remove(test_file)

    def test_empty_password_name(self):
        # проверка обработки ошибок при вводе пустого имени пароля
        passwords = [{"name": "", "password": "test_password"}]
        test_file = "test_passwords.json"

        # сохранение паролей в файл
        with open(test_file, "w") as file:
            json.dump(passwords, file, indent=4)

        # загрузка паролей из файла
        with open(test_file, "r") as file:
            loaded_passwords = json.load(file)

        # проверка наличия пустого имени
        self.assertTrue(any(p["name"] == "" for p in loaded_passwords), "Ожидалось наличие пустого имени пароля")

        # удаление тестового файла после завершения теста
        os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
