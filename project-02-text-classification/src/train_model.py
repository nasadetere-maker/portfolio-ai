# Обучение модели для классификации текстов
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np

print("Загружаем датасет и токенизатор...")
dataset = load_dataset("stanfordnlp/imdb")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

print("Токенизируем данные...")
tokenized_datasets = dataset.map(tokenize_function, batched=True)

print("Загружаем модель DistilBERT...")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# Метрики для оценки качества
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = np.mean(predictions == labels)
    return {"accuracy": accuracy}

print("Настраиваем параметры обучения...")
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_steps=100,
    report_to="none",
)

print("Создаём Trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"].shuffle(seed=42).select(range(5000)),
    eval_dataset=tokenized_datasets["test"].select(range(1000)),
    compute_metrics=compute_metrics,  # Убрали tokenizer=tokenizer
)

print("\n🚀 Начинаем обучение...")
trainer.train()

print("\n💾 Сохраняем модель...")
trainer.save_model("./model")
tokenizer.save_pretrained("./model")

print("\n✅ Обучение завершено! Модель сохранена в папке './model'")