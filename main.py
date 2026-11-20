from storage import load_data, save_data
from datetime import datetime


data = load_data()


# МЕНЮ
def show_menu():
    print("\n" + "=" * 35)
    print("       Личный Б.джет")
    print("=" * 35)
    print("1. Добавить доход")
    print("2. Добавить расход")
    print("3. Показать баланс")
    print("4. Расходы по категориям")
    print("5. Самая затратная категория")
    print("6. Установить месячный лимит")
    print("7. Показать месячный лимит")
    print("0. Выход")
    print("=" * 35)

# ВВОД СУММЫ


def get_amount():
    try:
        amount = float(input("Введите сумму: "))

        if amount <= 0:
            print("Сумма должна быть больше нуля!")
            return None

        return amount

    except ValueError:
        print("Ошибка! Введите число.")
        return None


# ВЫБОР КАТЕГОРИИ


def get_category():
    categories = [
        "Еда",
        "Транспорт",
        "Развлечения",
        "Одежда",
        "Учеба",
        "Другое"
    ]

    print("\nКатегории:")

    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    try:
        choice = int(input("Выберите категорию: "))

        if 1 <= choice <= len(categories):
            return categories[choice - 1]

        else:
            print("Такой категории нет!")
            return None

    except ValueError:
        print("Введите номер категории!")
        return None



# ДОБАВЛЕНИЕ ОПЕРАЦИ

def add_operation(operation_type):
    amount = get_amount()

    if amount is None:
        return

    category = get_category()

    if category is None:
        return

    operation = {
        "type": operation_type,
        "amount": amount,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    data["operations"].append(operation)

    save_data(data)

    if operation_type == "income":
        print("\nДоход успешно добавлен!")

    else:
        print("\nРасход успешно добавлен!")

        check_limit()


# ПОДСЧЕТ БАЛАНСА

def calculate_balance():
    balance = 0

    for operation in data["operations"]:

        if operation["type"] == "income":
            balance += operation["amount"]

        elif operation["type"] == "expense":
            balance -= operation["amount"]

    return balance


def show_balance():
    balance = calculate_balance()

    print("\n" + "-" * 35)
    print(f"Ваш текущий баланс: {balance:,.2f} сум")
    print("-" * 35)

# РАСХОДЫ ПО КАТЕГОРИЯМ


def category_expenses():
    expenses = {}

    for operation in data["operations"]:

        if operation["type"] == "expense":

            category = operation["category"]

            if category not in expenses:
                expenses[category] = 0

            expenses[category] += operation["amount"]

    if not expenses:
        print("\nРасходов пока нет.")
        return

    print("\nРасходы по категориям:")

    for category, amount in expenses.items():
        print(f"{category}: {amount:,.2f} сум")


# САМАЯ ЗАТРАТНАЯ КАТЕГОРИЯ

def most_expensive_category():
    expenses = {}

    for operation in data["operations"]:

        if operation["type"] == "expense":

            category = operation["category"]

            if category not in expenses:
                expenses[category] = 0

            expenses[category] += operation["amount"]

    if not expenses:
        print("\nРасходов пока нет.")
        return

    category = max(expenses, key=expenses.get)

    print("\nСамая затратная категория:")
    print(f"{category} — {expenses[category]:,.2f} сум")


# МЕСЯЧНЫЙ ЛИМИТ


def set_monthly_limit():
    try:
        limit = float(input("Введите месячный лимит расходов: "))

        if limit <= 0:
            print("Лимит должен быть больше нуля!")
            return

        data["monthly_limit"] = limit

        save_data(data)

        print(f"\nЛимит установлен: {limit:,.2f} сум")

        check_limit()

    except ValueError:
        print("Ошибка! Введите число.")


# РАСХОДЫ ТЕКУЩЕГО МЕСЯЦА


def get_month_expenses():
    current_month = datetime.now().strftime("%Y-%m")

    total = 0

    for operation in data["operations"]:

        if operation["type"] == "expense":

            if operation["date"].startswith(current_month):
                total += operation["amount"]

    return total


# ПРОВЕРКА ЛИМИТА

def check_limit():
    limit = data["monthly_limit"]

    if limit <= 0:
        return

    expenses = get_month_expenses()

    print(f"\nРасходы за текущий месяц: {expenses:,.2f} сум")
    print(f"Месячный лимит: {limit:,.2f} сум")

    if expenses > limit:
        print("ВНИМАНИЕ! Вы превысили месячный лимит!")

    elif expenses == limit:
        print("Вы достигли месячного лимита!")

    else:
        remaining = limit - expenses
        print(f"Осталось до лимита: {remaining:,.2f} сум")


# ПОКАЗ ЛИМИТА 

def show_monthly_limit():
    limit = data["monthly_limit"]

    if limit <= 0:
        print("\nМесячный лимит еще не установлен.")
        return

    expenses = get_month_expenses()

    print("\n" + "-" * 35)
    print(f"Месячный лимит: {limit:,.2f} сум")
    print(f"Расходы за месяц: {expenses:,.2f} сум")
    print(f"Остаток лимита: {limit - expenses:,.2f} сум")
    print("-" * 35)

    if expenses > limit:
        print("ВНИМАНИЕ! Лимит превышен!")


# ГЛАВНЫЙ ЦИКЛ

while True:

    show_menu()

    try:
        choice = int(input("Выберите действие: "))

        if choice == 1:
            add_operation("income")

        elif choice == 2:
            add_operation("expense")

        elif choice == 3:
            show_balance()

        elif choice == 4:
            category_expenses()

        elif choice == 5:
            most_expensive_category()

        elif choice == 6:
            set_monthly_limit()

        elif choice == 7:
            show_monthly_limit()

        elif choice == 0:
            print("\nПрограмма закрыта. До свидания!")
            break

        else:
            print("Неверный пункт меню!")

    except ValueError:
        print("Ошибка! Введите число!! ")