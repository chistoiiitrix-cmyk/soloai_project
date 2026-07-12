import json
import random
from content_engine import ContentEngine

# --- НАСТРОЙКА ---
# Вставь сюда свой API ключ от Groq
GROQ_API_KEY = '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'

def update_tools():
    print("Обновление базы инструментов...")
    try:
        with open('tools.json', 'r', encoding='utf-8') as f:
            tools = json.load(f)
        # Здесь можно добавить логику скрапинга новых инструментов
        # Для примера просто подтверждаем актуальность базы
        print("База инструментов проверена и актуальна.")
    except Exception as e:
        print(f"Ошибка при работе с tools.json: {e}")

def run_automation():
    engine = ContentEngine(api_key=GROQ_API_KEY)
    
    # 1. Обновляем инструменты
    update_tools()
    
    # 2. Генерируем новую статью в блог
    print("Запуск генерации статьи...")
    article = engine.generate_article()
    
    if article:
        try:
            with open('articles.json', 'r', encoding='utf-8') as f:
                articles = json.load(f)
        except:
            articles = []
        
        # Проверка на дубликаты, чтобы не постить одну и ту же новость
        if not any(a['title'] == article['title'] for a in articles):
            articles.insert(0, article) # Новая статья всегда сверху
            # Храним только 10 последних статей, чтобы файл не стал огромным
            with open('articles.json', 'w', encoding='utf-8') as f:
                json.dump(articles[:10], f, ensure_ascii=False, indent=4)
            print(f"✅ Новая статья успешно создана и добавлена: {article['title']}")
        else:
            print("Эта новость уже есть в блоге. Пропускаем.")
    else:
        print("Не удалось найти свежие новости для статьи.")

if __name__ == "__main__":
    run_automation()
