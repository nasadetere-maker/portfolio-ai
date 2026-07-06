# 🎨 AI Content Marketing Assistant

**Проект 3: Автоматизация создания контента с помощью AI**

---

## 📌 Описание проекта

AI-ассистент для автоматической генерации маркетингового контента на базе **n8n** и **Ollama** (локальный AI).

### Что умеет:
- ✍️ Генерировать посты для социальных сетей
- 📝 Создавать статьи и email-рассылки  
- 🤖 Работать **локально** (без интернета, бесплатно)
-  Быстро масштабироваться на разные типы контента

---

## 🏗️ Архитектура

### Технологии:
- **n8n** — оркестрация workflows
- **Ollama** — локальный AI-сервер (модель Llama3)
- **HTTP Request API** — взаимодействие с Ollama

---

## 🚀 Быстрый старт

### 1. Установи зависимости

**Установи n8n:**
```bash
npm install -g n8n
1. Установи Ollama:
Скачай: https://ollama.ai/download
Установи и запусти приложение
Скачай модель:ollama pull llama3
2. Запусти Ollama ollama serve
3. Запусти n8n
Открой в браузере: http://localhost:5678
4. Импортируй workflow
В n8n нажми Import from File
Выбери файл: workflows/ai-content-generator-ollama.json
Workflow загрузится
5. Протестируй
Нажми "Execute workflow"
AI сгенерирует пост про кофе (или другую тему)
Готово! 🎉
хостинг
💡 Примеры использования
Генерация поста про кофе:
Input: topic: "кофе"
Output:
Good morning, coffee lovers!
There's nothing quite like the perfect cup of joe to start your day off right...
#coffee #coffeeaddict #morningmotivation #caffeinekick📚 Документация
Case Study: docs/case-study.md
Workflow JSON: workflows/ai-content-generator-ollama.json
🔗 Полезные ссылки
n8n: https://n8n.io
Ollama: https://ollama.ai
Llama3: https://ollama.ai/library/llama3
Автор: Natalia
Дата: Июль 2026
**Статус проекта:** MVP с известными проблемами  
> Проект остановлен на этапе отладки подключения к Ollama.  
> Требуется архитектурный рефакторинг.  
> [Подробнее](docs/case-study.md#-известные-проблемы-не-решены)
