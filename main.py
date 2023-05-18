import logging
import os
from datetime import timedelta
from aiogram.utils import executor

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
filename = "data.txt"
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


def read_data_from_file() -> Dict[str, int]:
    if not os.path.isfile(filename):
        # Return default values if the file doesn't exist
        return {"minutes": 0, "rub": 0}

    with open(filename, 'r') as file:
        lines = file.readlines()
        numeric_minutes = ''.join(filter(str.isdigit, lines[0]))
        numeric_rub = ''.join(filter(str.isdigit, lines[1]))
        return {"minutes": int(numeric_minutes), "rub": int(numeric_rub)}


def write_data_from_file(minutes, rub) -> None:
    with open(filename, 'w') as file:
        file.write(f'{minutes} minutes\n')
        file.write(f'{rub} rub\n')


@dp.message_handler(regexp=r'^SAVED:.*')
async def handle_saved_message(message: types.Message):
    data = read_data_from_file()
    lines = message.text.split('\n')[1:]  # Exclude the first line ("SAVED:")
    saved_time = timedelta(minutes=data["minutes"])
    saved_money = data["rub"]
    for line in lines:
        line = line.strip()
        if 'hour' in line:
            hours = int(line.split()[0])
            saved_time += timedelta(hours=hours)
        elif 'minutes' in line:
            minutes = int(line.split()[0])
            saved_time += timedelta(minutes=minutes)
        elif 'rub' in line:
            rub = int(line.split()[0])
            saved_money += rub

    # Format the saved time
    total_minutes = saved_time.seconds // 60
    hours = saved_time.seconds // 3600
    minutes = (saved_time.seconds % 3600) // 60
    formatted_time = f'{hours} hours {minutes} minutes'

    write_data_from_file(minutes=total_minutes,  rub=saved_money)

    # Generate the response message
    response = f'Saved {formatted_time} and {saved_money} rub'
    await message.reply(response)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)