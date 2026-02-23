#!/usr/bin/env python3

import pathlib

current_dir = pathlib.Path(__file__).parent

def total_salary(filename: str) -> tuple[float, float]:
    total = 0.0
    count = 0

    p = current_dir / filename
    if p.exists() and p.is_file():
        with open(p, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    salary = float(line.strip().split(",")[1])
                    total += salary
                    count += 1
                except (ValueError, IndexError):
                    continue
    else:
        raise FileNotFoundError(
            f"Не можу зчитати файл '{filename}'. Перевірте, чи файл існує та чи вказано правильний шлях."
        )
    average = total / count if count > 0 else 0.0
    return total, average

try:
    total, average = total_salary("salary_file.txt")
    print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
except FileNotFoundError as error:
    print(error)
