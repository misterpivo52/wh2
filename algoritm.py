import random

result = []

def add(x, y):
    for i in range(x):
        result.append(y)
    return result

if __name__ == '__main__':
    while True:
        try:
            x = int(input("Кількість (0 щоб завершити): "))
            if x == 0:
                break
            y = int(input("Об'єкт: "))
            add(x, y)
        except ValueError:
            print("Введи число!")

    print("Список:", result)

    random.shuffle(result)
    print("Перемішаний:", result)

    unique_result = list(dict.fromkeys(result))
    print("рейтинг", unique_result)

