#!/usr/bin/env python3

# Topic 4. Homework
# Author: Mykola Mazurenko

from datetime import datetime, timedelta

def get_upcoming_birthdays(birthdays, days_ahead=7):
    today = datetime.today().date()
    upcoming = []

    for user in birthdays:
        birthday_this_year = datetime.strptime(user["birthday"], "%Y.%m.%d").date().replace(year=today.year)
        if today <= birthday_this_year <= today + timedelta(days=days_ahead):
            upcoming.append((user["name"], user["birthday"]))
        else:
            birthday_next_year = birthday_this_year.replace(year=today.year + 1)
            if today <= birthday_next_year <= today + timedelta(days=days_ahead):
                upcoming.append((user["name"], user["birthday"]))
    return upcoming

users = [
    {"name": "John Doe", "birthday": "1985.02.20"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]

upcoming_birthdays = get_upcoming_birthdays(users, 7)
print("Список привітань на цьому тижні:", upcoming_birthdays)
