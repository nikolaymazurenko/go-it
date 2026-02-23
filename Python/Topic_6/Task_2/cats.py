#!/usr/bin/env python3

import pathlib
from pprint import pprint

current_dir = pathlib.Path(__file__).parent

def get_cats_info(filename: str):
    cats_info: list[dict[str, str | int]] = []

    p = current_dir / filename
    if p.exists() and p.is_file():
        with open(p, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    cat_id, name, age = line.strip().split(",")
                    cats_info.append({"id": cat_id, "name": name, "age": int(age)})
                except (ValueError, IndexError):
                    continue
    else:
        raise FileNotFoundError(
            f"Не можу зчитати файл '{filename}'. Перевірте, чи файл існує та чи вказано правильний шлях."
        )
    return cats_info

try:
    cats_info = get_cats_info("cats_file.txt")
    pprint(cats_info, sort_dicts=False)
except FileNotFoundError as error:
    print(error)
