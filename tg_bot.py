import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройки (заменяются на реальные токены)
API_TOKEN = 'YOUR_TG_BOT_TOKEN'
SITE_URL = 'https://your-site.github.io'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, бро! 🚀\nЯ помогу тебе найти лучший AI-инструмент для любой задачи.\n\nПопробуй команды:\n/tools - Все инструменты\n/find [запрос] - Поиск конкретного AI\n/daily - Топ инструментов на сегодня")

@dp.message_handler(commands=['tools'])
async def list_tools(message: types.Message):
    await message.reply(f"Все наши находки собраны здесь: {SITE_URL}")

@dp.message_handler(commands=['daily'])
async def daily_top(message: types.Message):
    # В реальности берем рандомно из tools.json
    await message.reply("🔥 Топ дня:\n1. GigaChat (тексты)\n2. Midjourney (арт)\n3. Perplexity (поиск)\n\nПодробности на сайте!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
