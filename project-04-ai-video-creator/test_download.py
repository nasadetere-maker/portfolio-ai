import os
import requests
from dotenv import load_dotenv

load_dotenv()
PEXELS_KEY = os.getenv("PEXELS_API_KEY")

print("="*60)
print("🧪 ТЕСТ СКАЧИВАНИЯ ВИДЕО PEXELS")
print("="*60)

# 1. Ищем видео
print("\n1️⃣ ПОИСК ВИДЕО...")
url = "https://api.pexels.com/videos/search"
headers = {"Authorization": PEXELS_KEY}
params = {"query": "ocean", "per_page": 1}

response = requests.get(url, headers=headers, params=params)
print(f"   Статус API: {response.status_code}")

if response.status_code == 200:
    videos = response.json()["videos"]
    if videos:
        video_url = videos[0]["video_files"][0]["link"]
        print(f"   ✅ Видео найдено")
        print(f"   URL: {video_url[:80]}...")
        
        # 2. Пробуем скачать разными способами
        print("\n2️⃣ ПРОБУЕМ СКАЧАТЬ...")
        
        # Способ 1: Простой GET
        print("\n   Способ 1: Простой GET запрос")
        try:
            r1 = requests.get(video_url, timeout=10)
            print(f"   Статус: {r1.status_code}")
            print(f"   Размер: {len(r1.content)} байт")
            if r1.status_code == 200 and len(r1.content) > 1000:
                print("   ✅ РАБОТАЕТ!")
            else:
                print("   ❌ Не работает")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
        
        # Способ 2: С заголовками
        print("\n   Способ 2: С заголовками браузера")
        headers2 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Authorization": PEXELS_KEY
        }
        try:
            r2 = requests.get(video_url, headers=headers2, timeout=10)
            print(f"   Статус: {r2.status_code}")
            print(f"   Размер: {len(r2.content)} байт")
            if r2.status_code == 200 and len(r2.content) > 1000:
                print("   ✅ РАБОТАЕТ!")
            else:
                print("   ❌ Не работает")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            
        # Способ 3: С сессией
        print("\n   Способ 3: С сессией")
        session = requests.Session()
        session.headers.update({
            "Authorization": PEXELS_KEY,
            "User-Agent": "Mozilla/5.0"
        })
        try:
            r3 = session.get(video_url, timeout=10)
            print(f"   Статус: {r3.status_code}")
            print(f"   Размер: {len(r3.content)} байт")
            if r3.status_code == 200 and len(r3.content) > 1000:
                print("   ✅ РАБОТАЕТ!")
            else:
                print("   ❌ Не работает")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    else:
        print("   ❌ Видео не найдено")
else:
    print(f"   ❌ Ошибка API: {response.status_code}")
    print(f"   Ответ: {response.text}")

print("\n" + "="*60)
input("Нажми Enter чтобы выйти...")