# Загрузка датасета IMDB для сентимент-анализа
from datasets import load_dataset

print("Загружаем датасет IMDB...")

# Пробуем загрузить с полным именем репозитория
try:
    dataset = load_dataset("stanfordnlp/imdb")
    print("✅ Загружено с 'stanfordnlp/imdb'")
except:
    # Если не получилось, пробуем просто 'imdb'
    print("Пробуем альтернативный источник...")
    dataset = load_dataset("imdb")
    print("✅ Загружено с 'imdb'")

print(f"\nРазмер датасета:")
print(f"  Train: {len(dataset['train'])} примеров")
print(f"  Test: {len(dataset['test'])} примеров")

print(f"\nПервые 5 примеров из train:")
for i in range(5):
    text = dataset['train'][i]['text'][:100]  # первые 100 символов
    label = dataset['train'][i]['label']
    sentiment = "позитивный" if label == 1 else "негативный"
    print(f"\n{i+1}. [{sentiment}]")
    print(f"   Текст: {text}...")