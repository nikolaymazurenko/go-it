#!/usr/bin/env python3

# Topic 4. Homework 3
# Author: Mykola Mazurenko

import re

def normalize_phone(phone_number) -> str:
    digits = re.sub(r'\D', '', phone_number)
    if len(digits) == 10:
        return f"+38{digits}"
    elif len(digits) == 12 and digits.startswith("380"):
        return f"+{digits}"

raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)