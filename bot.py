import json
import os
from content_engine import ContentEngine

# --- НАСТРОЙКА ---
# ОБЯЗАТЕЛЬНО ВСТАВЬ СВОЙ КЛЮЧ СЮДА
GROQ_API_KEY = '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' 

def update_tools():
    print("🛠 Обновление базы инструментов...")
    try:
        if os.path.exists('tools.json'):
            with open('tools.json', 'r', encoding='utf-8') as f:
                json.load(f)
            print("✅ База инструментов в порядке.")
        else:
            # Создаем пустой файл, если его нет
            with open('tools.json', 'w', encoding='utf-8') as f:
                json.dump([], f)
            print("✅ Создана новая база инструментов.")
    except Exception as e:
        print(f"⚠️ Ошибка tools.json: {e}")

def run_automation():
    print("🚀 Запуск процесса автоматизации...")
    engine = ContentEngine(api_key=GROQ_API_KEY)
    
    # 1. Инструменты
    update_tools()
    
    # 2. Статьи
    article = engine.generate_//article() if hasattr(engine, 'generate_//article') else engine.generate_article()
    # Чтобы избежать любой ошибки с именами, вызываем напрямую проверенный метод:
    article = engine.generate_article()
    
    if article:
        try:
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
        print(f"💥 Критическая ошибка: {e}")
