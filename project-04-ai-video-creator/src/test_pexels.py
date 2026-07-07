import requests
import os
from dotenv import load_dotenv

load_dotenv()
PEXELS_KEY = os.getenv("PEXELS_API_KEY")

print("🔍 ТЕСТ PEXELS API")
print("=" * 50)
print(f"API Key: {PEXELS_KEY[:20]}..." if PEXELS_KEY else "❌ API Key не найден!")
print()

# Тест 1: Проверка API
url = "https://api.pexels.com/videos/search"
headers = {"Authorization": PEXELS_KEY}
params = {"query": "ocean", "per_page": 1}

print("📡 Отправка запроса...")
try:
    response = requests.get(url, headers=headers, params=params, timeout=10)
    print(f"✅ Статус: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        videos = data.get("videos", [])
        print(f"📹 Найдено видео: {len(videos)}")
        
        if videos:
            video = videos[0]
            print(f"\n🎬 Первое видео:")
            print(f"   ID: {video.get('id')}")
            print(f"   Duration: {video.get('duration')} sec")
            
            video_files = video.get("video_files", [])
            print(f"   Файлов: {len(video_files)}")
            
            if video_files:
                for vf in video_files[:2]:
                    print(f"   - {vf.get('quality')}: {vf.get('link')[:60]}...")
                    
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n" + "=" * 50)
input("Нажми Enter чтобы выйти...")