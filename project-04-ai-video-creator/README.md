# 🎬 AI Video Creator

Автоматический генератор видео с AI-озвучкой. Создаёт короткие видеоролики из стоковых материалов и синтезированного голоса.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Возможности

- ✅ **Автоматический поиск видео** на Pexels (бесплатная библиотека стоковых видео)
- ✅ **AI-озвучка текста** через Microsoft Edge TTS (бесплатно, без ограничений)
- ✅ **Поддержка русского и английского** языков
- ✅ **Словарь синонимов** для популярных тем (15+ категорий)
- ✅ **Красивый GUI** на CustomTkinter (тёмная тема)
- ✅ **Автоматический монтаж** видео с наложением аудио
- ✅ **Простой интерфейс** - достаточно ввести тему и текст

## 📦 Установка


```bash
git clone https://github.com/nasadetere-maker/portfolio-ai.git
cd portfolio-ai/project-04-ai-video-creator

# Установи зависимости
pip install -r requirements.txt
3. Настрой API ключ
Получи бесплатный API ключ на Pexels API
Создай файл .env в корне проекта
Добавь ключ:PEXELS_API_KEY=твой_ключ_здесь

🎯 Использование

Запуск GUI
python src/gui.py
Пример:
🎬 AI VIDEO CREATOR
========================================
Введите тему для видео: nature
Введите текст для озвучки: Природа — это удивительный мир вокруг нас.

🔍 Ищу видео по теме: nature...
✅ Видео найдено!
⬇️ Скачиваю...
🎤 Генерирую голос...
🎬 Монтирую видео...
✨ ГОТОВО! Видео сохранено: output/nature_video.mp4
Изменение голоса
В файле src/gui.py найди строку:
python
1
Доступные голоса:
Русский: ru-RU-SvetlanaNeural, ru-RU-DmitryNeural
Английский: en-US-JennyNeural, en-US-GuyNeural, en-GB-SoniaNeural
🛠 Технологии
Pexels API — бесплатные стоковые видео
Microsoft Edge TTS — синтез речи (бесплатно, без лимитов)
MoviePy — обработка и монтаж видео
CustomTkinter — современный GUI для Python
Requests — HTTP-запросы к API
🔑 Получение API ключа
Зарегистрируйся на Pexels.com
Перейди в Pexels API
Нажми "Sign Up" и создай аккаунт
Скопируй свой API ключ
Добавь его в файл .env
Это бесплатно и занимает 2 минуты!
🐛 Решение проблем
Ошибка "Видео не найдено"
Проверь интернет-соединение
Попробуй другую тему (на английском)
Убедись что API ключ правильный
Ошибка "Не удалось скачать видео"
Pexels может временно блокировать запросы
Подожди 5 минут и попробуй снова
Проверь что API ключ активен
Ошибка монтирования
Убедись что установлены все зависимости
Попробуй переустановить moviePy: pip install --upgrade moviepy
📄 Лицензия
MIT License — используй как хочешь!
👤 Автор
Nataly
GitHub: @nasadetere-maker
🙏 Благодарности
Pexels — бесплатные стоковые видео
Edge TTS — синтез речи от Microsoft
MoviePy — монтаж видео на Python
CustomTkinter — современный GUI
⭐ Если понравилось — поставь звезду на GitHub!
Создано с ❤️ для Portfolio AI Projects