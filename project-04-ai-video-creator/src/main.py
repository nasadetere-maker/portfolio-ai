import os
import requests
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip
from dotenv import load_dotenv

# Загружаем ключи из .env
load_dotenv()
PEXELS_KEY = os.getenv("PEXELS_API_KEY")

# Словарь синонимов для популярных тем
SYNONYMS = {
    'кофе': ['coffee', 'cafe', 'espresso', 'latte'],
    'природа': ['nature', 'forest', 'landscape', 'wilderness'],
    'технологии': ['technology', 'computer', 'coding', 'ai', 'artificial intelligence'],
    'бизнес': ['business', 'office', 'meeting', 'work', 'corporate'],
    'спорт': ['sport', 'fitness', 'gym', 'running', 'workout'],
    'еда': ['food', 'cooking', 'restaurant', 'meal', 'cuisine'],
    'путешествия': ['travel', 'adventure', 'vacation', 'tourism'],
    'музыка': ['music', 'concert', 'singing', 'performance'],
    'космос': ['space', 'galaxy', 'stars', 'universe', 'astronomy'],
    'океан': ['ocean', 'sea', 'waves', 'beach', 'marine'],
    'город': ['city', 'urban', 'street', 'architecture'],
    'животные': ['animals', 'wildlife', 'pets', 'dogs', 'cats'],
    'машины': ['cars', 'vehicles', 'driving', 'automotive'],
    'мода': ['fashion', 'style', 'clothing', 'design'],
    'здоровье': ['health', 'wellness', 'medical', 'fitness'],
}

def get_video_url(topic):
    """Ищет видео на Pexels с поддержкой русских тем и синонимов"""
    
    # Проверяем синонимы
    search_terms = SYNONYMS.get(topic.lower(), [topic])
    
    print(f"\n📚 Поиск по темам: {', '.join(search_terms)}")
    
    for term in search_terms:
        print(f"🔍 Ищу видео: {term}...")
        
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": PEXELS_KEY}
        params = {
            "query": term, 
            "per_page": 1, 
            "orientation": "landscape",
            "size": "medium"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                videos = response.json()["videos"]
                if videos:
                    video_url = videos[0]["video_files"][0]["link"]
                    print(f"✅ Найдено по запросу '{term}'!")
                    return video_url
        except Exception as e:
            print(f"⚠️  Ошибка при поиске '{term}': {e}")
            continue
    
    print("\n❌ Видео не найдено.")
    print("\n💡 ПОПУЛЯРНЫЕ ТЕМЫ:")
    print("   • Природа: nature, forest, ocean, mountains")
    print("   • Технологии: technology, coding, ai, computer")
    print("   • Бизнес: business, office, meeting, work")
    print("   • Еда: coffee, food, cooking, restaurant")
    print("   • И другие на английском!")
    return None

def download_file(url, filepath):
    """Скачивает файл с проверкой"""
    print(f"⬇️ Скачиваю видео...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✅ Видео скачано: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")
        return False

async def generate_audio(text, filepath):
    """Генерирует голос с поддержкой русского языка"""
    print(f"🎤 Генерирую голос...")
    
    # Определяем язык текста
    voice = "ru-RU-SvetlanaNeural"  # Русский по умолчанию
    if text.isascii():
        voice = "en-US-JennyNeural"  # Английский если текст на английском
        print("   (Английский голос)")
    else:
        print("   (Русский голос)")
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filepath)
        
        # Проверяем что файл создан
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print(f"✅ Аудио сохранено: {filepath}")
            return True
        else:
            print("❌ Ошибка: аудио файл пустой")
            return False
    except Exception as e:
        print(f"❌ Ошибка генерации голоса: {e}")
        return False

def create_video(video_path, audio_path, output_path):
    """Склеивает видео и аудио"""
    print(f"🎬 Монтирую видео...")
    
    try:
        # Загружаем файлы
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Проверяем длительности
        print(f"   Видео: {video.duration:.1f} сек")
        print(f"   Аудио: {audio.duration:.1f} сек")
        
        # Обрезаем видео под длину аудио
        if audio.duration > video.duration:
            print("   ⚠️  Аудио длиннее видео, повторяю видео...")
            final_duration = audio.duration
            final_video = video.subclipped(0, video.duration)
        else:
            final_duration = audio.duration
            final_video = video.subclipped(0, audio.duration)
        
        final_video = final_video.with_audio(audio)
        
        # Сохраняем (ИСПРАВЛЕНО: убрал verbose и logger)
        final_video.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac",
            fps=24
        )
        
        # Закрываем файлы
        video.close()
        audio.close()
        final_video.close()
        
        print(f"✨ ГОТОВО! Видео сохранено: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка монтажа: {e}")
        return False

async def main():
    print("\n" + "="*50)
    print("🎬 AI VIDEO CREATOR")
    print("   Автоматическая генерация видео")
    print("="*50)
    
    # Показываем доступные темы
    print("\n📚 ДОСТУПНЫЕ ТЕМЫ (можно вводить на русском):")
    for ru, en_list in list(SYNONYMS.items())[:5]:
        print(f"   • {ru.capitalize()}: {', '.join(en_list[:3])}")
    print("   • И любые другие на английском...")
    print("\n" + "-"*50)
    
    # Ввод темы
    topic = input("\n📝 Введите тему для видео: ").strip()
    if not topic:
        print("❌ Тема не введена!")
        return
    
    script_text = input("📝 Введите текст для озвучки: ").strip()
    if not script_text:
        print("❌ Текст не введён!")
        return
    
    # Создаём папки
    os.makedirs("assets", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("examples", exist_ok=True)
    
    print("\n" + "="*50)
    print("🚀 НАЧИНАЮ ГЕНЕРАЦИЮ...")
    print("="*50)
    
    # 1. Ищем и скачиваем видео
    video_url = get_video_url(topic)
    if not video_url:
        return
    
    video_path = "assets/temp_video.mp4"
    if not download_file(video_url, video_path):
        return
    
    # 2. Генерируем голос
    audio_path = "assets/temp_audio.mp3"
    if not await generate_audio(script_text, audio_path):
        return
    
    # 3. Создаём финальное видео
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_')
    output_filename = f"output/{safe_topic}_video.mp4"
    
    if create_video(video_path, audio_path, output_filename):
        # Показываем размер файла
        file_size = os.path.getsize(output_filename) / (1024 * 1024)
        print(f"\n📊 Размер файла: {file_size:.1f} MB")
        print(f"📁 Путь: {os.path.abspath(output_filename)}")
        
        # Предлагаем скопировать в examples
        copy_to_examples = input("\n💾 Скопировать в examples/ для портфолио? (y/n): ").lower()
        if copy_to_examples == 'y':
            import shutil
            examples_path = f"examples/{safe_topic}_video.mp4"
            shutil.copy2(output_filename, examples_path)
            print(f"✅ Скопировано в: {examples_path}")
    
    # 4. Чистим временные файлы
    try:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        print("\n✅ Временные файлы удалены.")
    except PermissionError:
        print("\n⚠️  Временные файлы не удалены (заняты процессом).")
        print("   Можно удалить вручную позже.")
    
    print("\n" + "="*50)
    print("✨ ГЕНЕРАЦИЯ ЗАВЕРШЕНА!")
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        print("💡 Попробуйте запустить ещё раз")