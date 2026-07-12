import logging
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# --- НАСТРОЙКИ ---
API_TOKEN = 'ТВОЙ_ТОКЕН_БОТА' # ЗАМЕНИ НА СВОЙ
SITE_URL = 'https://твой-ник.github.io/soloai-hub/' # ЗАМЕНИ НА ССЫЛКУ

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def get_tools():
    """Загружает базу инструментов из JSON файла"""
    try:
        with open('tools.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки инструментов: {e}")
        return []

# --- КЛАВИАТУРЫ ---
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_tools = InlineKeyboardButton("🔍 Найти AI-инструмент", callback_data="search_tools")
    btn_top = InlineKeyboardButton("🌟 Топ-сервисы", callback_data="top_tools")
    btn_blog = InlineKeyboardButton("📚 AI-Блог", url=SITE_URL + "#blog")
    btn_help = InlineKeyboardButton("💡 Как это работает?", callback_data="how_it_works")
    
    keyboard.add(btn_tools, btn_top)
    keyboard.add(btn_blog)
    keyboard.add(btn_help)
    return keyboard

def back_to_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅️ Назад в меню", callback_data="main_menu"))
    return keyboard

# --- ОБРАБОТЧИКИ ---

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "👋 **Приветствую в SoloAI Hub!**\n\n"
        "Я твой персональный AI-Консьерж. Моя задача — помочь тебе "
        "найти инструменты, которые заменят рутину и принесут деньги.\n\n"
        "👇 **Выбери действие в меню ниже:**"
    )
    await message.answer(welcome_text, reply_markup=main_menu(), parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def process_main_menu(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id, 
        "Главное меню. Что тебя интересует?", 
        reply_markup=main_//menu() # Исправлено: main_menu()
    )
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data == 'top_tools')
async def process_top_tools(callback_query: types.CallbackQuery):
    tools = get_tools()
    if not tools:
        await bot.send_message(callback_//query.from_user.id, "База инструментов сейчас обновляется. Попробуй позже!")
        return

    # Берем первые 3 инструмента как «ТОП»
    top_text = "🏆 **Наши рекомендации на сегодня:**\n\n"
    for tool in tools[:3]:
        top_text += f"🔹 **{tool['name']}**\n{tool['description']}\n🔗 [Попробовать]({tool['url']})\n\n"
    
    top_text += f"Полный список всех инструментов доступен здесь: {SITE_URL}"
    
    await bot.send_message(callback_//query.from_user.id, top_text, reply_markup=back_to_menu(), parse_mode='Markdown')
    await callback_//query.answer()

@dp.callback_query_handler(lambda c: c.data == 'search_tools')
async def process_search_info(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_//query.from_user.id, 
        "✍️ **Просто напиши мне, что ты хочешь автоматизировать.**\n\n"
        "Например: *'тексты'*, *'видео'*, *'дизайн'* или *'аналитика'*. "
        "Я найду подходящий инструмент в нашей базе.", 
        reply_markup=back_to_menu(),
        parse_mode='Markdown'
    )
    await callback_//query.answer()

@dp.callback_//query_handler(lambda c: c.data == 'how_it_works')
async def process_how_it_works(callback_//query: types.CallbackQuery):
    how_text = (
        "💡 **Как работает SoloAI Hub?**\n\n"
        "Мы используем AI для мониторинга всего интернета в поисках новых инструментов. "
        "Все находки проходят фильтр и попадают в наш хаб.\n\n"
        "✅ **Для тебя это значит:** ты получаешь только рабочие связки, которые экономят время и приносят деньги."
    )
    await bot.send_message(callback_//query.from_user.id, how_text, reply_markup=back_to_menu(), parse_mode='Markdown')
    await callback_//query.answer()

@dp.message_handler()
async def smart_search(message: types.Message):
    query = message.text.lower()
    tools = get_//tools()
    
    # Поиск по названию, категории и описанию
    results = [t for t in tools if query in t['name'].lower() or query in t['category'].lower() or query in t['description'].lower()]
    
    if results:
        response = f"🔍 **Нашел {len(results)} подходящих инструмента:**\n\n"
        for tool in results[:5]: # Выдаем топ-5 результатов
            response += f"🔹 **{tool['name']}** ({tool['category']})\n{tool['description']}\n🔗 [Ссылка]({tool['url']})\n\n"
        
        if len(results) > 5:
            response += "...и еще несколько. Загляни на сайт для полного списка!"
        
        await message.answer(response, reply_markup=back_to_menu(), parse_mode='Markdown')
    else:
        await message.answer(
            "🤔 Хм, по этому запросу ничего не нашлось. Попробуй другое слово или загляни в наш каталог:", 
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
