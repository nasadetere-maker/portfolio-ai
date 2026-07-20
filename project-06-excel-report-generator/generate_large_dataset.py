import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Настройки генерации
NUM_ROWS = 1000
START_DATE = datetime.now() - timedelta(days=90)
END_DATE = datetime.now()

# Списки для генерации
PRODUCTS = [
    'Ноутбук ASUS', 'Ноутбук Lenovo', 'Ноутбук HP', 'Ноутбук Dell', 'Ноутбук Apple',
    'iPhone 15', 'iPhone 14', 'Samsung Galaxy S24', 'Samsung Galaxy A54', 'Xiaomi 14',
    'iPad Air', 'iPad Pro', 'Samsung Tab S9', 'Lenovo Tab', 'Xiaomi Pad',
    'Apple Watch 9', 'Samsung Watch', 'Xiaomi Band', 'Garmin Forerunner', 'Huawei Watch',
    'AirPods Pro', 'Sony WH-1000XM5', 'JBL Tune', 'Samsung Buds', 'Xiaomi Buds',
    'Клавиатура Logitech', 'Мышь Logitech', 'Монитор Dell', 'Монитор LG', 'Веб-камера',
    'Принтер HP', 'Принтер Canon', 'Сканер', 'Флешка 64GB', 'Внешний диск 1TB',
    'SSD Samsung', 'Оперативная память', 'Процессор AMD', 'Видеокарта NVIDIA', 'Блок питания'
]

CITIES = [
    'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань',
    'Нижний Новгород', 'Челябинск', 'Самара', 'Омск', 'Ростов-на-Дону',
    'Уфа', 'Красноярск', 'Воронеж', 'Пермь', 'Волгоград'
]

CATEGORIES = [
    'Ноутбуки', 'Смартфоны', 'Планшеты', 'Умные часы', 'Наушники',
    'Периферия', 'Мониторы', 'Комплектующие', 'Принтеры', 'Аксессуары'
]

REGIONS = [
    'Центральный', 'Северо-Западный', 'Сибирский', 'Уральский', 'Приволжский',
    'Южный', 'Дальневосточный'
]

MANAGERS = [
    'Иванов А.', 'Петрова М.', 'Сидоров К.', 'Козлова Е.', 'Новиков Д.',
    'Морозова А.', 'Волков С.', 'Лебедева Н.', 'Соколов И.', 'Попова О.'
]

def generate_price(product):
    """Генерация реалистичной цены в зависимости от товара"""
    base_prices = {
        'Ноутбук': (45000, 150000),
        'iPhone': (60000, 130000),
        'Samsung Galaxy': (30000, 90000),
        'Xiaomi': (15000, 40000),
        'iPad': (40000, 90000),
        'Tab': (20000, 60000),
        'Watch': (15000, 45000),
        'Band': (2000, 5000),
        'AirPods': (15000, 25000),
        'Sony': (25000, 35000),
        'JBL': (3000, 8000),
        'Клавиатура': (2000, 15000),
        'Мышь': (1000, 8000),
        'Монитор': (15000, 50000),
        'Принтер': (8000, 25000),
        'SSD': (3000, 12000),
        'Оперативная': (2000, 15000),
        'Процессор': (10000, 50000),
        'Видеокарта': (20000, 80000),
    }
    
    for key, (min_p, max_p) in base_prices.items():
        if key in product:
            return random.randint(min_p, max_p)
    return random.randint(1000, 30000)

def generate_data():
    """Генерация набора данных"""
    print("🔄 Генерация 1000 строк данных...")
    
    data = []
    
    for i in range(NUM_ROWS):
        # Случайная дата
        delta_days = random.randint(0, 90)
        sale_date = START_DATE + timedelta(days=delta_days)
        
        # Случайный товар и его характеристики
        product = random.choice(PRODUCTS)
        category = None
        for cat in CATEGORIES:
            if any(word in product for word in ['Ноутбук', 'iPad', 'Tab', 'Монитор', 'Принтер', 'SSD', 'Оперативная', 'Процессор', 'Видеокарта']):
                category = cat
                break
        if not category:
            category = random.choice(CATEGORIES)
        
        # Генерация данных
        quantity = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            weights=[40, 25, 15, 8, 5, 3, 2, 1, 0.5, 0.5]
        )[0]
        
        price = generate_price(product)
        discount = random.choices(
            [0, 5, 10, 15, 20, 25],
            weights=[50, 20, 15, 8, 5, 2]
        )[0]
        
        final_price = int(price * (100 - discount) / 100)
        revenue = final_price * quantity
        
        city = random.choice(CITIES)
        region = random.choice(REGIONS)
        manager = random.choice(MANAGERS)
        
        # Способ оплаты
        payment_method = random.choices(
            ['Карта', 'Наличные', 'Безнал', 'Кредит', 'Рассрочка'],
            weights=[40, 20, 25, 10, 5]
        )[0]
        
        # Статус заказа
        status = random.choices(
            ['Завершён', 'В обработке', 'Отменён', 'Возврат'],
            weights=[75, 15, 7, 3]
        )[0]
        
        # ID заказа
        order_id = f"ORD-{2024000 + i}"
        
        # Клиент
        client_names = ['ООО Техно', 'ИП Иванов', 'ЗАО Связь', 'ООО Гаджет', 'ИП Петров', 'АО Цифра']
        client = random.choice(client_names)
        
        data.append({
            'ID_заказа': order_id,
            'Дата': sale_date.strftime('%Y-%m-%d'),
            'Время': sale_date.strftime('%H:%M:%S'),
            'Товар': product,
            'Категория': category,
            'Количество': quantity,
            'Цена_до_скидки': price,
            'Скидка_процент': discount,
            'Цена_итого': final_price,
            'Выручка': revenue,
            'Город': city,
            'Регион': region,
            'Менеджер': manager,
            'Клиент': client,
            'Способ_оплаты': payment_method,
            'Статус': status,
            'Комментарий': random.choice([
                '', '', '', '',  # 40% без комментария
                'Срочная доставка', 'Подарочная упаковка', 'Корпоративный заказ',
                'Самовывоз', 'Доставка на дом', 'Клиент постоянный',
                'Первый заказ', 'Возврат в течение 14 дней', 'Гарантия расширенная'
            ])
        })
    
    df = pd.DataFrame(data)
    
    # Сортировка по дате
    df = df.sort_values('Дата')
    
    return df

def save_data(df):
    """Сохранение данных в CSV и Excel"""
    # CSV
    csv_path = 'data/large_sales_data.csv'
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"✅ CSV сохранён: {csv_path}")
    
    # Excel
    excel_path = 'data/large_sales_data.xlsx'
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Продажи', index=False)
        
        # Сводка по категориям
        category_summary = df.groupby('Категория').agg({
            'Выручка': ['sum', 'mean', 'count'],
            'Количество': 'sum'
        }).round(2)
        category_summary.columns = ['Общая выручка', 'Средний чек', 'Кол-во заказов', 'Всего товаров']
        category_summary.to_excel(writer, sheet_name='По категориям')
        
        # Сводка по городам
        city_summary = df.groupby('Город').agg({
            'Выручка': 'sum',
            'ID_заказа': 'count'
        }).sort_values('Выручка', ascending=False)
        city_summary.columns = ['Выручка', 'Заказы']
        city_summary.to_excel(writer, sheet_name='По городам')
        
        # Сводка по менеджерам
        manager_summary = df.groupby('Менеджер').agg({
            'Выручка': 'sum',
            'ID_заказа': 'count'
        }).sort_values('Выручка', ascending=False)
        manager_summary.columns = ['Выручка', 'Заказы']
        manager_summary.to_excel(writer, sheet_name='По менеджерам')
    
    print(f"✅ Excel сохранён: {excel_path}")

def print_stats(df):
    """Вывод статистики по данным"""
    print("\n" + "="*60)
    print("📊 СТАТИСТИКА СГЕНЕРИРОВАННЫХ ДАННЫХ")
    print("="*60)
    
    print(f"📦 Всего записей: {len(df)}")
    print(f"📅 Период: {df['Дата'].min()} — {df['Дата'].max()}")
    print(f"🏷️  Уникальных товаров: {df['Товар'].nunique()}")
    print(f" Городов: {df['Город'].nunique()}")
    print(f"👥 Менеджеров: {df['Менеджер'].nunique()}")
    
    total_revenue = df['Выручка'].sum()
    avg_check = df['Цена_итого'].mean()
    
    print(f"\n💰 Общая выручка: {total_revenue:,.0f} ₽")
    print(f"💵 Средний чек: {avg_check:,.0f} ₽")
    print(f"📈 Среднее кол-во в заказе: {df['Количество'].mean():.2f}")
    
    print(f"\n🏆 Топ-5 товаров по выручке:")
    top_products = df.groupby('Товар')['Выручка'].sum().nlargest(5)
    for i, (prod, rev) in enumerate(top_products.items(), 1):
        print(f"   {i}. {prod}: {rev:,.0f} ₽")
    
    print(f"\n🌍 Топ-5 городов по выручке:")
    top_cities = df.groupby('Город')['Выручка'].sum().nlargest(5)
    for i, (city, rev) in enumerate(top_cities.items(), 1):
        print(f"   {i}. {city}: {rev:,.0f} ₽")

if __name__ == "__main__":
    # Создаём папку data если нет
    import os
    os.makedirs('data', exist_ok=True)
    
    # Генерация
    df = generate_data()
    
    # Сохранение
    save_data(df)
    
    # Статистика
    print_stats(df)
    
    print("\n✅ Готово! Можно запускать генератор отчётов.")