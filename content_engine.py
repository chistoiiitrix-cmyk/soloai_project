import json
import requests
import feedparser
import random
from datetime import datetime

class ContentEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key
        # Источники свежих AI-новостей
        self.sources = [
            "https://www.producthunt.com/feed",
            "https://techcrunch.com/category/artificial-intelligence/feed/"
        ]

    def fetch_real_news(self):
        print("Поиск свежих новостей в сети...")
        all_news = []
        for url in self.sources:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:3]: # Берем по 3 последние записи
                    all_news.append({
                        "title": entry.title, 
                        "link": entry.link, 
                        "summary": entry.get('summary', 'Нет описания')
                    })
            except Exception as e:
                print(f"Ошибка при чтении {url}: {e}")
        return all_news

    def ai_rewrite(self, text, mode="tg"):
        if not self.api_key:
            return f"Новость: {text[:100]}... Подробности на сайте!"
        
        try:
            if mode == "tg":
                prompt = f"Перепиши это для Telegram. Сделай текст коротким, дерзким, с эмодзи и призывом перейти на сайт. Текст: {text}"
            else:
                prompt = f"Напиши полноценную SEO-статью для блога на основе этого текста: {text}. " \
                          f"Структура: Заголовок, Введение, Основные преимущества (списком), Итог. " \
                          f"Стиль: Экспертный, но доступный. Язык: 
