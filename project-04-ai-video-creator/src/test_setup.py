import os
import requests
import asyncio
import edge_tts
from dotenv import load_dotenv

# Загружаем ключи из .env
load_dotenv()
PEXELS_KEY = os.getenv("PEXELS_API_KEY")

def test_pexels():
    print("🔍 Тестируем Pexels API...")
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_KEY}
    params = {"query": "nature", "per_page": 1}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200 and response.json()["videos"]:
        video_data = response.json()["videos"][0]
        # Берем первое доступное видео в хорошем качестве
        video_url = video_data["video_files"][0]["link"]
        print(f"✅ Pexels OK. Ссылка получена.")
        return video_url
    else:
        print(f"❌ Ошибка Pexels: {response.text}")
        return None

async def test_tts():
    print("🎤 Тестируем генерацию голоса...")
    try:
        # Используем бесплатный голос Microsoft Edge
        communicate = edge_tts.Communicate("Привет, это тест работы генератора голоса.", "ru-RU-SvetlanaNeural")
        await communicate.save("assets/test_voice.mp3")
        print("✅ Голос OK. Файл сохранен.")
        return True
    except Exception as e:
        print(f"❌ Ошибка голоса: {e}")
        return False

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    print("🚀 Запуск проверки компонентов...\n")
    
    # 1. Проверяем видео
    video_url = test_pexels()
    if video_url:
        print("️ Скачиваю тестовое видео...")
        r = requests.get(video_url)
        with open("assets/test_video.mp4", "wb") as f:
            f.write(r.content)
        print("✅ Видео сохранено в assets/test_video.mp4")
    
    # 2. Проверяем голос
    asyncio.run(test_tts())
    
    print("\n🎉 Если видишь галочки ✅ — фундамент готов! Переходим к монтажу.")