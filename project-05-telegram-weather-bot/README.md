
# 🤖 Telegram Weather Bot

Telegram бот для проверки погоды в любом городе мира. Работает на базе n8n workflow automation.

![n8n](https://img.shields.io/badge/n8n-automation-ff6d5a)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4)
![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-API-blue)

## 🌟 Возможности

- ✅ **Погода в любом городе** — просто отправь название города
- ✅ **Подробная информация** — температура, влажность, ветер, давление
- ✅ **Прогноз на несколько дней** — узнай погоду наперед
- ✅ **Автоматические уведомления** — можно настроить расписание
- ✅ **Поддержка °C и °F** — выбирай удобные единицы

## 📋 Что внутри

### Технологии
- **n8n** — workflow automation (бесплатно, self-hosted)
- **Telegram Bot API** — интерфейс бота
- **OpenWeatherMap API** — данные о погоде (бесплатный тариф)

### Как это работает
Пользователь → Telegram Bot → n8n Webhook → OpenWeatherMap API → n8n → Telegram

1. Пользователь отправляет название города боту
2. Telegram отправляет сообщение на webhook в n8n
3. n8n делает запрос к OpenWeatherMap API
4. Получает данные о погоде
5. Форматирует и отправляет ответ пользователю

## 🚀 Быстрый старт

### 1. Установи n8n

**Локально (Node.js):**
```bash
npm install n8n -g
n8n start
Или Docker:
bash
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
2. Создай Telegram бота
Открой @BotFather в Telegram
Отправь /newbot
Придумай имя и username
Скопируй токен (выглядит как 123456:ABC-DEF1234...)
3. Получи API ключ OpenWeatherMap
Зарегистрируйся на OpenWeatherMap
Перейди в API Keys
Скопируй ключ
4. Настрой workflow
Открой n8n в браузере (http://localhost:5678)
Импортируй workflow из файла workflows/weather-bot-workflow.json
Открой узлы и настрой:
Telegram Trigger — вставь токен бота
OpenWeatherMap — вставь API ключ
Активируй workflow (переключатель вверху)
5. Настрой webhook
В узле Telegram Webhook нажми "Create Webhook" — n8n сам настроит URL.
6. Готово!
Отправь своему боту название города, например: Moscow или London
🔧 Настройка workflow
Основные узлы:
Telegram Trigger — получает сообщения
OpenWeatherMap — запрашивает погоду
Code/Function — форматирует ответ
Telegram — отправляет ответ
Дополнительные возможности:
/start — команда приветствия
/help — справка
Автоматические уведомления — через Cron узел
📊 Примеры использования
Запрос погоды:
Пользователь: Moscow
Бот: 🌤 Москва
     Температура: 22°C
     Ощущается как: 20°C
     Влажность: 65%
     Ветер: 3 м/с
     Команды:
     /start — Начать работу
/help — Справка
🐛 Решение проблем
Бот не отвечает
Проверь что webhook активен: https://api.telegram.org/bot<TOKEN>/getWebhookInfo
Убедись что workflow активирован в n8n
Ошибка API
Проверь API ключ OpenWeatherMap
У бесплатного тарифа лимит 60 вызовов/минуту
Не находит город
Проверь название города на английском
Используй формат: City,Country (например: Moscow,RU)
🔐 Безопасность
Никогда не публикуй:
Токен Telegram бота
API ключ OpenWeatherMap
Файл .env
Добавь эти файлы в .gitignore!
📚 Ресурсы
n8n Documentation
Telegram Bot API
OpenWeatherMap API
🤝 Вклад
Pull requests приветствуются!
📄 Лицензия
MIT License
Создано с ❤️ с использованием n8n