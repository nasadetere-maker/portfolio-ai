# Предсказание настроения текста
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

print("Загружаем модель...")
model_path = "./model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=-1)
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities[0][predicted_class].item()
    
    sentiment = "позитивный 😊" if predicted_class == 1 else "негативный 😞"
    return sentiment, confidence

# Тестируем на примерах
test_texts = [
    "I absolutely love this movie! The acting was fantastic and the story was amazing.",
    "This was the worst film I have ever seen. Terrible acting and boring plot.",
    "The movie was okay, not great but not bad either.",
    "What a wonderful experience! I would recommend this to everyone!",
    "I hate this. Complete waste of time and money."
]

print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ ПРЕДСКАЗАНИЙ")
print("="*60)

for text in test_texts:
    sentiment, confidence = predict_sentiment(text)
    print(f"\nТекст: {text[:70]}...")
    print(f"Настроение: {sentiment}")
    print(f"Уверенность: {confidence*100:.1f}%")

print("\n" + "="*60)
print("\nВведи свой текст для анализа (или 'quit' для выхода):")

while True:
    user_text = input("\n> ")
    if user_text.lower() == 'quit':
        break
    sentiment, confidence = predict_sentiment(user_text)
    print(f"Настроение: {sentiment}")
    print(f"Уверенность: {confidence*100:.1f}%")