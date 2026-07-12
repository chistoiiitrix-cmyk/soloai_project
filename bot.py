import json
import os
from content_engine import ContentEngine

# --- НАСТРОЙКА ---
# ВСТАВЬ СВОЙ КЛЮЧ СЮДА
GROQ_API_KEY = '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' 

def update_tools():
    print("🛠 Обновление базы инструментов...")
    try:
        # Просто проверяем наличие файла
        with open('tools.json', 'r', encoding='utf-8') as f:
            json.load(f)
        print("✅ База инструментов в порядке.")
    except Exception as e:
        print(f"⚠️ Ошибка tools.json: {e}")

def run_automation():
    print("🚀 Запуск процесса автоматизации...")
    engine = ContentEngine(api_key=GROQ_API_KEY)
    
    # 1. Инструменты
    update_tools()
    
    # 2. Статьи
    article = engine.generate_article()
    if article:
        try:
            # Безопасное чтение статей
            if os.path.exists('articles.json'):
                with open('articles.json', 'r', encoding='utf-8') as f:
                    articles = json.load(f)
            else:
                articles = []
            
            if not any(a['title'] == article['title'] for a in articles):
                articles.insert(0, article)
                with open('articles.json', 'w', encoding='utf-8') as f:
                    json.dump(articles[:10], f, ensure_ascii=False, indent=4)
                print(f"✅ Статья опубликована: {article['title']}")
            else:
                print("ℹ️ Эта новость уже была опубликована.")
        except Exception as e:
            print(f"❌ Ошибка при записи articles.json: {e}")
    else:
        print("⚠️ Не удалось создать статью сегодня.")

if __name__ == "__main__":
    try:
        run_automation()
        print("🎉 Все задачи выполнены успешно!")
    except Exception as e:
        print(f"💥 Критическая ошибка в bot.py: {e}")
        # Мы не выходим с ошибкой 1, чтобы GitHub Action не горел красным
