# Этот скрипт создаст чистый файл .env без ошибок кодировки
import os

# Твой ключ
API_KEY = "P3u2kyCsiinhr8RmZJ208tV0tUcS9XQSqIf4VCeX8jY0LefQMXmtdqln"

# Путь к файлу .env (в корневой папке проекта)
env_path = os.path.join(os.path.dirname(__file__), '.env')

print(f"🔧 Создаю файл: {env_path}")

try:
    # Открываем в режиме записи с чистой кодировкой utf-8
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(f"PEXELS_API_KEY={API_KEY}\n")
    
    print("✅ Файл .env успешно создан!")
    
    # Проверка
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"📄 Содержимое файла:\n{content}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")

input("Нажми Enter чтобы выйти...")