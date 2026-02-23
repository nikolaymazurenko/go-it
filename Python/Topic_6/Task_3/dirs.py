#!/usr/bin/env python3

from pathlib import Path
import sys
from colorama import init, Fore

init(autoreset=True)

def get_dir_info(dir_path: str, formating: str = ""):
    directory = Path(dir_path)
    spacer = " " * 4
    if directory.exists() and directory.is_dir():
        try:
            for path in directory.iterdir():
                if path.is_dir():
                    print(f"{formating}{Fore.LIGHTBLUE_EX}{path.name}")
                    get_dir_info(str(path), formating + spacer)
                elif path.is_file():
                    print(f"{formating}{Fore.LIGHTGREEN_EX}{path.name}")
        except PermissionError:
            print(f"{formating}[Немає доступу]: {directory}")
    else:
        print(f"Не можу зчитати директорію '{dir_path}'. Перевірте, чи директорія існує та чи вказано правильний шлях.")
        return

if len(sys.argv) < 2:
    print("Вкажіть шлях до директорії: python dirs.py <path>")
else:
    get_dir_info(sys.argv[1])
