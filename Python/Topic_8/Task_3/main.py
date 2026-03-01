#!/usr/bin/env python3

import sys

def parse_log_line(line: str) -> dict:
    parts = line.strip().split(' ', 3)
    date, time, level, message = parts
    return {
        'date': date,
        'time': time,
        'timestamp': f"{date} {time}",
        'level': level,
        'message': message
    }

def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                log_entry = parse_log_line(line)
                if log_entry:
                    logs.append(log_entry)
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log.get('level').upper() == level.upper()]

def count_logs_by_level(logs: list) -> dict:
    counts = {}
    for log in logs:
        level = log.get('level')
        if level:
            counts[level] = counts.get(level, 0) + 1
    return counts

def display_log_counts(counts: dict):
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    level_order = ['INFO', 'DEBUG', 'ERROR', 'WARNING']
    for level in level_order:
        if level in counts:
            print(f"{level:<16} | {counts[level]}")
    print()

def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_файлу_логів> [рівень]")
        print("Рівні: INFO, ERROR, DEBUG, WARNING")
        sys.exit(1)
    file_path = sys.argv[1]
    logs = load_logs(file_path)
    if not logs:
        print("Помилка: Немає логів для обробки.")
        sys.exit(1)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)
    if len(sys.argv) > 2:
        filter_level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, filter_level)
        if filtered_logs:
            print(f"Деталі логів для рівня '{filter_level.upper()}':")
            for log in filtered_logs:
                print(f"{log['timestamp']} - {log['message']}")
        else:
            print(f"Немає записів з рівнем '{filter_level.upper()}'.")

if __name__ == "__main__":
    main()