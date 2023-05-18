import os
from typing import Dict

filename = "data.txt"


def read_data_from_file() -> Dict[str, int]:
    if not os.path.isfile(filename):
        # Return default values if the file doesn't exist
        return {"minutes": 0, "rub": 0}

    with open(filename, 'r') as file:
        lines = file.readlines()
        numeric_minutes = ''.join(filter(str.isdigit, lines[0]))
        numeric_rub = ''.join(filter(str.isdigit, lines[1]))
        return {"minutes": int(numeric_minutes), "rub": int(numeric_rub)}


def write_data_to_file(minutes, rub) -> None:
    with open(filename, 'w') as file:
        file.write(f'{minutes} minutes\n')
        file.write(f'{rub} rub\n')