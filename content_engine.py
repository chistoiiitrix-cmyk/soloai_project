import json
import requests
import feedparser # Нужно будет добавить в requirements.txt
import random

class ContentEngine:
    def __init__(self, api_key="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"):
        self.api_key = api_key
        # Список RSS-лент для сбора AI-новостей
        self.sources = [
            "https://www.producthunt.com/feed",
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://futurepedia.io/rss" # Если доступно
        ]

    def fetch_real_news(self):
        print("Поиск свежих новостей...")
        all_news = []
        for url in self.sources:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:3]: # Берем по 3 последние записи из каждого источника
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
            # Если ключа нет, используем упрощенный шаблон (заглушка)
            if mode == "tg":
                return f"🔥 Свежий инструмент! {text[:50]}... Подробности на нашем сайте! 🚀"
            return f"<h1>Обзор инструмента</h1><p>{text}</p>"

        # Здесь логика запроса к API (например, Groq или OpenAI)
        # Пример для Groq/OpenAI-compatible API:
        try:
            prompt = (
                f"Перепиши этот текст для {'Telegram' if mode == 'tg' else 'SEO-статьи'}. "
                f"Сделай его привлекательным, полезным и продающим. "
                f"Текст: {text}"
            )
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

    def run_full_cycle(self, tg_bot=None):
        news_list = self.fetch_real_news()
        if not news_list:
            print("Новостей не найдено.")
            return

        # Выбираем одну случайную новость для 오늘의 поста
        news = random.choice(news_list)
        print(f"Обработка новости: {news['title']}")

        raw_text = f"{news['title']}. {news['summary']}"
        
        # Генерируем контент
        tg_post = self.ai_rewrite(raw_text, mode="tg")
        web_article = self.ai_rewrite(raw_text, mode="web")

        # 1. Сохраняем статью на сайт (в новый файл articles.json)
        self.save_article(news, web_article)

        # 2. Пушим в ТГ
        if tg_bot:
            tg_bot.send_message(tg_post)

        print("Цикл завершен успешно!")

    def save_article(self, news, content):
        try:
            with open('articles.json', 'r', encoding='utf-8') as f:
                articles = json.load(f)
        except:
            articles = []

        articles.append({
            "title": news['title'],
            "content": content,
            "link": news['link'],
            "date": "2026-07-11" # В реальности datetime.now()
        })

        with open('articles.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Для теста запустим без ключа
    engine = ContentEngine(api_key="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")
    engine.run_full_cycle()
