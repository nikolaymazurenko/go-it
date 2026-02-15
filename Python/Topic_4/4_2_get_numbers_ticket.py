#!/usr/bin/env python3

# Topic 4. Homework 2
# Author: Mykola Mazurenko

import random;

def get_numbers_ticket(min, max, quantity) -> list[int]:
    if min > max:
        raise ValueError("Мінімальне значення не може бути більше за максимальне значення")
    elif quantity <= 0:
        raise ValueError("Кількість не може бути від'ємною або нульовою")
    elif quantity > (max - min + 1):
        raise ValueError("Кількість не може бути більшою за діапазон чисел")
    else:
        res = random.sample(range(min, max + 1), quantity)
        return sorted(res)

min_value = int(input("Введіть мінімальне значення в діапазоні від 1 до 1000: "))
max_value = int(input("Введіть максимальне значення в діапазоні від 1 до 1000: "))
quantity_value = int(input("Введіть кількість чисел для генерації: "))

lottery_numbers = get_numbers_ticket(min_value, max_value, quantity_value)
print("Ваші лотерейні числа:", lottery_numbers)