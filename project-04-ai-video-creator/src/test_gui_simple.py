import os
import sys
import requests

# Читаем .env
def load_env_manually():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    print(f"🔍 Ищу .env: {env_path}")
    
    if not os.path.exists(env_path):
        print("❌ .env не найден")
        return None
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
                if key == "PEXELS_API_KEY":
                    print(f"✅ API ключ найден: {value[:20]}...")
                    return value
    return None

PEXELS_KEY = load_env_manually()

if not PEXELS_KEY:
    print("❌ КЛЮЧ НЕ НАЙДЕН!")
    sys.exit(1)

print("\n🧪 ТЕСТ PEXELS API")
print("=" * 50)

# Тест запроса
topic = "ocean"
url = "https://api.pexels.com/videos/search"
headers = {
    "Authorization": PEXELS_KEY,
    "User-Agent": "Mozilla/5.0"
}
params = {"query": topic, "per_page": 3, "orientation": "landscape"}

print(f"📡 Отправка запроса к Pexels...")
print(f"   Тема: {topic}")

try:
    response = requests.get(url, headers=headers, params=params, timeout=10)
    print(f"✅ Статус ответа: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        videos = data.get("videos", [])
        print(f"📹 Найдено видео: {len(videos)}")
        
        if videos:
            print("\n✅ ВИДЕО НАЙДЕНЫ!")
            for i, video in enumerate(videos[:2], 1):
                print(f"\n🎬 Видео #{i}:")
                print(f"   ID: {video.get('id')}")
                print(f"   Duration: {video.get('duration')} sec")
                
                video_files = video.get("video_files", [])
                if video_files:
                    for vf in video_files[:1]:
                        print(f"   URL: {vf.get('link')[:80]}...")
        else:
            print("\n❌ ВИДЕО НЕ НАЙДЕНЫ")
            print(f"Ответ API: {data}")
    else:
        print(f"❌ Ошибка API: {response.status_code}")
        print(f"Текст ошибки: {response.text}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
input("Нажми Enter чтобы выйти...")