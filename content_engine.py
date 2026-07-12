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
            # Разные промпты для разных целей
            if mode == "tg":
                prompt = f"Перепиши это для Telegram. Сделай текст коротким, дерзким, с эмодзи и призывом перейти на сайт. Текст: {text}"
            else: # Режим для полноценной статьи в блог
                prompt = f"Напиши полноценную SEO-статью для блога на основе этого текста: {text}. " \
                          f"Структура: Заголовок, Введение, Основные преимущества (списком), Итог. " \
                          f"Стиль: Экспертный, но доступный. Язык: Русский."

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "llama3-8b-8192", 
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Ошибка AI: {e}")
            return "Ошибка генерации контента."

    def generate_article(self):
        news_list = self.fetch_real_news()
        if not news_list: return None

        news = random.choice(news_list)
        raw_text = f"{news['title']}. {news['summary']}"
        
        # Генерируем полноценную статью и краткий анонс (summary) для карточки на сайте
        full_content = self.ai_rewrite(raw_text, mode="web")
        summary = self.ai_rewrite(raw_text, mode="tg")[:150] + "..."

        return {
            "title": news['title'],
            "summary": summary,
            "content": full_content,
            "link": news['link'],
            "date": datetime.now().strftime("%Y-%m-%d")
        }
