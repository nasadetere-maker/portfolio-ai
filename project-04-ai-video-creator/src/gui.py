import os
import sys
import requests
import asyncio
import edge_tts
import customtkinter as ctk
from moviepy import VideoFileClip, AudioFileClip
from tkinter import messagebox
import threading
import queue
import time

def load_env_manually():
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'),
        os.path.join(os.getcwd(), '.env'),
        '.env'
    ]
    
    env_path = None
    for path in possible_paths:
        if os.path.exists(path):
            env_path = path
            break
    
    if not env_path:
        return None
    
    encodings = ['utf-8-sig', 'utf-8', 'cp1251', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(env_path, 'r', encoding=encoding) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
                        if key.strip() == "PEXELS_API_KEY":
                            return value.strip()
            break
        except:
            continue
    
    return None

print("🎬 AI Video Creator - Загрузка...")
PEXELS_KEY = load_env_manually()

if PEXELS_KEY:
    print(f"✅ PEXELS_API_KEY загружен")
else:
    print("❌ PEXELS_API_KEY НЕ ЗАГРУЖЕН!")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SYNONYMS = {
    'кофе': ['coffee', 'cafe', 'espresso'],
    'природа': ['nature', 'forest', 'landscape'],
    'технологии': ['technology', 'computer', 'coding'],
    'бизнес': ['business', 'office', 'meeting'],
    'спорт': ['sport', 'fitness', 'gym'],
    'еда': ['food', 'cooking', 'restaurant'],
    'путешествия': ['travel', 'adventure', 'vacation'],
    'музыка': ['music', 'concert', 'singing'],
    'космос': ['space', 'galaxy', 'stars'],
    'океан': ['ocean', 'sea', 'waves'],
    'город': ['city', 'urban', 'street'],
    'животные': ['animals', 'wildlife', 'pets'],
}

class VideoCreatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🎬 AI Video Creator")
        self.geometry("700x700")
        self.resizable(False, False)
        
        self.is_generating = False
        self.last_video_path = None
        self.msg_queue = queue.Queue()
        
        if not PEXELS_KEY:
            messagebox.showerror("Ошибка", "PEXELS_API_KEY не найден!")
        
        self.create_widgets()
        self.check_queue()
        
    def create_widgets(self):
        title = ctk.CTkLabel(self, text="🎬 AI Video Creator", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=15)
        
        subtitle = ctk.CTkLabel(self, text="Автоматическая генерация видео с AI-озвучкой", font=ctk.CTkFont(size=13))
        subtitle.pack(pady=(0, 20))
        
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(input_frame, text="📝 Тема видео:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        self.topic_entry = ctk.CTkEntry(input_frame, width=600, placeholder_text="На английском: nature, coffee, technology")
        self.topic_entry.pack(padx=15, pady=(0, 5))
        
        ctk.CTkLabel(input_frame, text="🗣 Текст для озвучки:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        self.text_entry = ctk.CTkTextbox(input_frame, width=600, height=80)
        self.text_entry.pack(padx=15, pady=(0, 15))
        self.text_entry.insert("0.0", "Введите текст для озвучки видео...")
        
        self.generate_btn = ctk.CTkButton(self, text="🚀 Сгенерировать видео", command=self.start_generation,
            font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="#28a745", hover_color="#218838")
        self.generate_btn.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self, text="Готов к работе ✅", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(10, 5))
        
        self.progress = ctk.CTkProgressBar(self, width=600)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        result_frame = ctk.CTkFrame(self)
        result_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(result_frame, text="📁 Результат:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.result_label = ctk.CTkLabel(result_frame, text="Пока нет сгенерированных видео", font=ctk.CTkFont(size=10), justify="left", wraplength=550)
        self.result_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        self.open_btn = ctk.CTkButton(result_frame, text="📂 Открыть папку", command=self.open_folder, state="disabled", width=200)
        self.open_btn.pack(pady=(0, 15))
        
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(log_frame, text="📋 Лог:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(log_frame, width=600, height=100, font=ctk.CTkFont(size=9))
        self.log_text.pack(padx=15, pady=(0, 15), fill="both", expand=True)
        self.log_text.configure(state="disabled")
        
    def check_queue(self):
        try:
            while True:
                msg_type, msg_data = self.msg_queue.get_nowait()
                
                if msg_type == "log":
                    self.log_text.configure(state="normal")
                    self.log_text.insert("end", msg_data + "\n")
                    self.log_text.see("end")
                    self.log_text.configure(state="disabled")
                elif msg_type == "status":
                    message, progress = msg_data
                    self.status_label.configure(text=message)
                    if progress is not None:
                        self.progress.set(progress)
                elif msg_type == "done":
                    self.is_generating = False
                    self.generate_btn.configure(state="normal", text="🚀 Сгенерировать видео")
                    success, result = msg_data
                    if success:
                        self.last_video_path = result['path']
                        self.result_label.configure(text=f"✅ {result['path']}\n📊 {result['size']:.1f} MB")
                        self.open_btn.configure(state="normal")
                        messagebox.showinfo("Успех!", f"Видео создано!\n\n{result['path']}")
                    else:
                        messagebox.showerror("Ошибка", result)
                elif msg_type == "error":
                    self.is_generating = False
                    self.generate_btn.configure(state="normal", text="🚀 Сгенерировать видео")
                    messagebox.showerror("Ошибка", msg_data)
                    
        except queue.Empty:
            pass
        
        self.after(100, self.check_queue)
        
    def log(self, message):
        self.msg_queue.put(("log", message))
        
    def update_status(self, message, progress=None):
        self.msg_queue.put(("status", (message, progress)))
        
    def start_generation(self):
        if self.is_generating:
            return
            
        topic = self.topic_entry.get().strip()
        text = self.text_entry.get("0.0", "end").strip()
        
        if not topic or not text or text == "Введите текст для озвучки видео...":
            messagebox.showwarning("Внимание", "Заполните тему и текст!")
            return
        
        if not PEXELS_KEY:
            messagebox.showerror("Ошибка", "PEXELS_API_KEY не настроен!")
            return
            
        self.is_generating = True
        self.generate_btn.configure(state="disabled", text="⏳ Генерация...")
        self.progress.set(0)
        self.log_text.delete("0.0", "end")
        
        thread = threading.Thread(target=self.generate_video, args=(topic, text), daemon=True)
        thread.start()
        
    def download_video(self, video_url, video_path):
        """Простое скачивание - как в тесте"""
        try:
            self.log("   Скачивание...")
            
            response = requests.get(video_url, timeout=30)
            
            if response.status_code == 200:
                with open(video_path, 'wb') as f:
                    f.write(response.content)
                
                file_size = os.path.getsize(video_path)
                self.log(f"   ✅ Скачано: {file_size / 1024:.1f} KB")
                
                if file_size > 10000:
                    return True
                else:
                    self.log(f"   ⚠️  Файл маленький: {file_size} байт")
                    return False
            else:
                self.log(f"   ❌ Статус: {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"   ❌ Ошибка: {str(e)[:60]}")
            return False
        
    def generate_video(self, topic, text):
        try:
            os.makedirs("output", exist_ok=True)
            os.makedirs("assets", exist_ok=True)
            
            self.update_status("🔍 Ищу видео...", 0.1)
            self.log(f"🔍 Поиск видео: {topic}")
            
            video_url = self.get_working_video_url(topic)
            
            if not video_url:
                self.update_status("❌ Видео не найдено", 0)
                self.log("❌ Не найдено рабочее видео")
                self.msg_queue.put(("done", (False, "Видео не найдено")))
                return
            
            self.log(f"✅ Видео найдено")
            
            self.update_status("⬇️ Скачиваю...", 0.25)
            self.log("⬇️ Скачивание видео...")
            
            video_path = "assets/temp_video.mp4"
            
            if not self.download_video(video_url, video_path):
                raise Exception("Не удалось скачать видео")
            
            self.update_status("🎤 Генерирую голос...", 0.5)
            self.log("🎤 Генерация голоса...")
            
            audio_path = "assets/temp_audio.mp3"
            voice = "ru-RU-SvetlanaNeural" if not text.isascii() else "en-US-JennyNeural"
            
            asyncio.run(self.generate_audio(text, audio_path, voice))
            self.log("✅ Голос готов")
            
            self.update_status("🎬 Монтирую...", 0.7)
            self.log("🎬 Монтаж видео...")
            
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).strip()
            safe_topic = safe_topic.replace(' ', '_')
            output_path = f"output/{safe_topic}_video.mp4"
            
            self.create_video_file(video_path, audio_path, output_path)
            self.log(f"✅ Видео создано")
            
            self.update_status("🧹 Очистка...", 0.9)
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except:
                pass
            
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            
            self.update_status("✨ Готово! ✅", 1.0)
            self.log(f"\n✨ ЗАВЕРШЕНО!")
            self.log(f"📊 Размер: {file_size:.1f} MB")
            
            self.msg_queue.put(("done", (True, {'path': output_path, 'size': file_size})))
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.msg_queue.put(("error", f"Не удалось создать видео:\n\n{e}"))
    
    def get_working_video_url(self, topic):
        """Ищет видео"""
        search_terms = SYNONYMS.get(topic.lower(), [topic])
        
        for term in search_terms:
            self.log(f"   Поиск: {term}")
            
            url = "https://api.pexels.com/videos/search"
            headers = {"Authorization": PEXELS_KEY}
            params = {"query": term, "per_page": 5, "orientation": "landscape"}
            
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code != 200:
                    self.log(f"   ❌ Ошибка API: {response.status_code}")
                    continue
                
                data = response.json()
                videos = data.get("videos", [])
                
                if not videos:
                    self.log(f"   ⚠️  Видео не найдено")
                    continue
                
                for i, video in enumerate(videos[:5], 1):
                    video_files = video.get("video_files", [])
                    if not video_files:
                        continue
                    
                    video_url = None
                    for vf in video_files:
                        quality = vf.get("quality", "").lower()
                        if quality in ["hd", "hls", "sd"]:
                            video_url = vf["link"]
                            break
                    
                    if not video_url and video_files:
                        video_url = video_files[0]["link"]
                    
                    if video_url:
                        self.log(f"   ✅ Найдено видео #{i}")
                        return video_url
                            
            except Exception as e:
                self.log(f"   ❌ Ошибка: {str(e)[:50]}")
                continue
        
        return None
    
    async def generate_audio(self, text, filepath, voice):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filepath)
    
    def create_video_file(self, video_path, audio_path, output_path):
        try:
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            if audio.duration > video.duration:
                final_video = video.subclipped(0, video.duration)
            else:
                final_video = video.subclipped(0, audio.duration)
            
            final_video = final_video.with_audio(audio)
            # ✅ ИСПРАВЛЕНО: убраны параметры verbose и logger
            final_video.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac", 
                fps=24
            )
            
            video.close()
            audio.close()
            final_video.close()
            
        except Exception as e:
            raise Exception(f"Ошибка монтажа: {e}")
    
    def open_folder(self):
        if self.last_video_path:
            os.startfile(os.path.dirname(self.last_video_path))

if __name__ == "__main__":
    app = VideoCreatorApp()
    app.mainloop()