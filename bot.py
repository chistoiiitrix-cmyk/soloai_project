import json
import random

def generate_ai_description(tool_name, category):
    templates = [
        f"{tool_name} — это прорыв в области {category}. Позволяет соло-предпринимателям автоматизировать рутину и сфокусироваться на росте.",
        f"Если вы работаете в {category}, {tool_name} станет вашим лучшим помощником для масштабирования операций.",
        f"Хватит тратить время на {category} вручную. {tool_name} использует AI, чтобы сделать всё за вас за секунды."
    ]
    return random.choice(templates)

def find_new_tools():
    mock_new_tools = [
        {"name": "AutoGPT", "category": "Автономные агенты", "niche": "Business"},
        {"name": "Copy.ai", "category": "Копирайтинг", "niche": "Marketing"},
        {"name": "Tally.so", "category": "Формы", "niche": "General"},
        {"name": "10Web", "category": "Сайты", "niche": "Design"}
    ]
    return random.choice(mock_new_tools)

def update_database():
    with open('tools.json', 'r', encoding='utf-8') as f:
        tools = json.load(f)
    
    new_tool_data = find_new_tools()
    
    if any(t['name'] == new_tool_data['name'] for t in tools):
        print("Инструмент уже существует. Пропускаем...")
        return

    # Генерация ID и структуры
    new_id = max([t['id'] for t in tools]) + 1 if tools else 1
    new_tool = {
        "id": new_id,
        "name": new_tool_data['name'],
        "niche": new_tool_data['niche'],
        "category": new_tool_data['category'],
        "description": generate_ai_description(new_tool_data['name'], new_tool_data['category']),
        "url": f"https://{new_tool_data['name'].lower().replace(' ', '')}.com?ref=your_id",
        "tags": ["AI", "автоматизация", "новое"]
    }
    
    tools.append(new_tool)
    
    with open('tools.json', 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=4)
    
    print(f"Успешно добавлен {new_tool['name']} в базу!")

if __name__ == "__main__":
    update_database()
