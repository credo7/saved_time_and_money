import logging
import os
from datetime import timedelta
from aiogram.utils import executor

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import utils

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(regexp=r'^SAVED:.*')
async def handle_saved_message(message: types.Message):
    data = utils.read_data_from_file()
    lines = message.text.split('\n')[1:]
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

    total_minutes = saved_time.seconds // 60
    hours = saved_time.seconds // 3600
    minutes = (saved_time.seconds % 3600) // 60
    formatted_time = f'{hours} hours {minutes} minutes'

    utils.write_data_to_file(minutes=total_minutes,  rub=saved_money)

    response = f'Saved {formatted_time} and {saved_money} rub'
    await message.reply(response)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)