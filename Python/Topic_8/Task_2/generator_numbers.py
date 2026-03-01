#!/usr/bin/env python3

from collections.abc import Callable
import re


def generator_numbers(text: str):
    for word in text.split():
        if re.match(r'^\d+(\.\d+)?$', word):
            yield float(word)

def sum_profit(text: str, func: Callable):
    total = 0
    for number in func(text):
        total += number
    return total

text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."

total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")