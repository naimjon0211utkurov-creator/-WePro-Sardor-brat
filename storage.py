import json
import os
FILE_NAME = "budget.json"


def load_data():
    if not os.path.exists(FILE_NAME):
        return {
            "operations": [],
            "monthly_limit": 0
        }

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except json.JSONDecodeError:
        print("Ошибка: файл JSON поврежден.")
        return {
            "operations": [],
            "monthly_limit": 0
        }

    except FileNotFoundError:
        print("Файл не найден.")
        return {
            "operations": [],
            "monthly_limit": 0
        }


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)