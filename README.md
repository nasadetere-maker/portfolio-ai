# Text Classification (NLP)

**Project 2 of my AI Engineering Portfolio**

## 📌 Описание проекта

Модель для **сентимент-анализа** текстов на английском языке. Определяет настроение отзыва: **позитивный** или **негативный**.

Обучена на датасете **IMDB Movie Reviews** (50,000 отзывов) с использованием модели **DistilBERT** (fine-tuning).

---

## 🏆 Результаты

| Метрика | Значение |
|---------|----------|
| **Accuracy** | **93%** ✅ |
| Модель | DistilBERT (66M параметров) |
| Эпохи обучения | 3 |
| Время обучения | ~60 минут |
| Датасет | 50,000 отзывов (IMDB) |

---

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
2. Загрузка датасета
python src/load_dataset.py
3. Предобработка данных
python src/preprocess_data.py
4. Обучение модели
python src/train_model.py
5. Предсказание на новых текстах
python src/predict.py
6. Запуск веб-интерфейса (Gradio)
python src/app.py
📂 Структура проекта
project-02-text-classification/
├── data/                  # Датасеты (не в Git)
├── model/                 # Обученная модель (не в Git)
├── results/               # Результаты обучения (не в Git)
├── screenshots/           # Скриншоты результатов
│   ├── day4-training-complete.png
│   └── day5-gradio-app.png
├── src/                   # Исходный код
│   ├── load_dataset.py    # Загрузка IMDB
│   ├── preprocess_data.py # Токенизация
│   ├── train_model.py     # Обучение модели
│   ├── predict.py         # Предсказания в терминале
│   └── app.py             # Gradio веб-интерфейс
├── case-study.md          # Подробная документация
├── README.md              # Описание проекта
├── requirements.txt       # Зависимости
└── .gitignore
🛠️ Технологии
Python 3.14
HuggingFace Transformers — модель DistilBERT
Datasets — загрузка IMDB
PyTorch — обучение нейросети
Gradio — веб-интерфейс
Git + GitHub — контроль версий
---

## 🌐 Онлайн-демо

Попробуй модель прямо сейчас:

👉 **[HuggingFace Spaces: Sentiment Analysis NLP](https://huggingface.co/spaces/nataly-nlp-dev/sentiment-analysis-nlp)**

---

## 🔗 Полезные ссылки

- **🎭 Демо:** [Попробовать модель](https://huggingface.co/spaces/nataly-nlp-dev/sentiment-analysis-nlp)
- **📚 Документация:** [case-study.md](case-study.md)
- **📦 Датасет:** [IMDB на HuggingFace](https://huggingface.co/datasets/stanfordnlp/imdb)

---

**Автор:** Natalia  
**Дата:** Июнь 2026  
**Статус:** ✅ Завершён