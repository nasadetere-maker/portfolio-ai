# Предобработка данных для классификации текстов
from datasets import load_dataset
from transformers import AutoTokenizer

print("Загружаем датасет IMDB...")
dataset = load_dataset("stanfordnlp/imdb")

print("Загружаем токенизатор DistilBERT...")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_function(examples):
    """Токенизация текста"""
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

print("Токенизируем данные...")
tokenized_datasets = dataset.map(tokenize_function, batched=True)

print(f"\nРазмер токенизированного датасета:")
print(f"  Train: {len(tokenized_datasets['train'])} примеров")
print(f"  Test: {len(tokenized_datasets['test'])} примеров")

print(f"\nПример токенизированного текста:")
sample = tokenized_datasets['train'][0]
print(f"  Input IDs (первые 20): {sample['input_ids'][:20]}")
print(f"  Attention mask (первые 20): {sample['attention_mask'][:20]}")
print(f"  Label: {sample['label']}")

print("\n✅ Предобработка завершена!")