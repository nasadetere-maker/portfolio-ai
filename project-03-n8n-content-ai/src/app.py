# Веб-интерфейс для классификации текстов (Gradio)
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

print("Загружаем модель...")
model_path = "./model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

def predict_sentiment(text):
    """Предсказание настроения текста"""
    if not text.strip():
        return "Введи текст для анализа", 0.0
    
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=-1)
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    confidence = probabilities[0][predicted_class].item()
    
    if predicted_class == 1:
        return "😊 Позитивный", round(confidence * 100, 1)
    else:
        return "😞 Негативный", round(confidence * 100, 1)

# Создаём интерфейс Gradio
demo = gr.Interface(
    fn=predict_sentiment,
    inputs=gr.Textbox(lines=3, placeholder="Введи текст на английском...", label="Текст отзыва"),
    outputs=[
        gr.Textbox(label="Настроение"),
        gr.Number(label="Уверенность (%)")
    ],
    title="🎭 Sentiment Analysis (NLP)",
    description="Модель DistilBERT, обученная на 50,000 отзывов IMDB. Точность: 93%",
    examples=[
        ["This movie was absolutely fantastic! Best film of the year!"],
        ["Terrible acting and boring plot. Waste of time."],
        ["The cinematography was beautiful but the story was weak."],
        ["I loved every minute of it. Highly recommended!"],
        ["Awful experience. Would never watch again."]
    ]
    # Убрали: allow_flagging="never" (устарело в новой версии)
)

if __name__ == "__main__":
    print("\n🚀 Запуск веб-интерфейса...")
    print("Открой браузер по адресу: http://127.0.0.1:7860")
    demo.launch()