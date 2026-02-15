#!/usr/bin/env python3

# Topic 4. Homework 1
# Author: Mykola Mazurenko

from datetime import datetime
import re

checking_date = input("Введіть дату у форматі (YYYY-MM-DD): ")

def get_days_from_today(date):
    if not re.match(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$', date):
        raise ValueError("Дата повинна бути у форматі YYYY-MM-DD і бути дійсною датою")
    else:
        today = datetime.today().date()
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        delta = today - target_date
        return delta.days

print(f"Кількість днів від сьогодні до {checking_date}: {get_days_from_today(checking_date)}")