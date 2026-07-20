import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ExcelReportGenerator:
    def __init__(self, data_path=None):
        self.data_path = data_path
        self.df = None
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def load_data(self, file_path):
        """Загрузка данных из файла"""
        print(f"📂 Загрузка файла: {file_path}")
        
        if file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path, encoding='utf-8-sig')
        elif file_path.endswith('.xlsx'):
            self.df = pd.read_excel(file_path)
        else:
            raise ValueError("Поддерживаются только CSV и Excel файлы")
        
        print(f"✅ Загружено {len(self.df)} строк, {len(self.df.columns)} столбцов")
        print(f"📋 Колонки: {', '.join(self.df.columns)}")
        return self.df
    
    def clean_data(self):
        """Очистка данных"""
        print("\n🧹 Очистка данных...")
        
        # Удаление дубликатов
        duplicates = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates()
        print(f"   Удалено дубликатов: {duplicates}")
        
        # Заполнение пропусков
        missing = self.df.isnull().sum()
        total_missing = missing.sum()
        self.df = self.df.fillna(0)
        print(f"   Заполнено пропусков: {total_missing}")
        
        return self.df
    
    def analyze_data_advanced(self):
        """Расширенный анализ данных"""
        print("\n" + "="*60)
        print(" РАСШИРЕННЫЙ АНАЛИЗ ДАННЫХ")
        print("="*60)
        
        if self.df is None:
            print("❌ Сначала загрузи данные!")
            return
        
        # 1. Основные метрики
        print("\n📈 ОСНОВНЫЕ МЕТРИКИ:")
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        print(f"   Числовых колонок: {len(numeric_cols)}")
        
        for col in numeric_cols[:5]:  # Первые 5 числовых колонок
            print(f"\n   📊 {col}:")
            print(f"      Сумма: {self.df[col].sum():,.2f}")
            print(f"      Среднее: {self.df[col].mean():,.2f}")
            print(f"      Медиана: {self.df[col].median():,.2f}")
            print(f"      Мин: {self.df[col].min():,.2f}")
            print(f"      Макс: {self.df[col].max():,.2f}")
            print(f"      Стд. отклонение: {self.df[col].std():,.2f}")
        
        # 2. Анализ выручки (если есть)
        revenue_col = None
        for col in ['Выручка', 'Revenue', 'Сумма', 'Total', 'Amount']:
            if col in self.df.columns:
                revenue_col = col
                break
        
        if revenue_col:
            print(f"\n💰 АНАЛИЗ ВЫРУЧКИ ({revenue_col}):")
            total_revenue = self.df[revenue_col].sum()
            avg_revenue = self.df[revenue_col].mean()
            median_revenue = self.df[revenue_col].median()
            
            print(f"   Общая выручка: {total_revenue:,.2f} ₽")
            print(f"   Средний чек: {avg_revenue:,.2f} ₽")
            print(f"   Медианный чек: {median_revenue:,.2f} ₽")
            print(f"   Всего транзакций: {len(self.df)}")
            
            # Процентили
            print(f"   25-й процентиль: {self.df[revenue_col].quantile(0.25):,.2f} ₽")
            print(f"   75-й процентиль: {self.df[revenue_col].quantile(0.75):,.2f} ₽")
        
        # 3. Анализ по категориям
        category_col = None
        for col in ['Категория', 'Category', 'категория']:
            if col in self.df.columns:
                category_col = col
                break
        
        if category_col and revenue_col:
            print(f"\n📦 АНАЛИЗ ПО КАТЕГОРИЯМ:")
            category_stats = self.df.groupby(category_col)[revenue_col].agg([
                'sum', 'mean', 'count', 'median'
            ]).sort_values('sum', ascending=False)
            
            for cat, row in category_stats.iterrows():
                print(f"\n   {cat}:")
                print(f"      Выручка: {row['sum']:,.2f} ₽")
                print(f"      Средний чек: {row['mean']:,.2f} ₽")
                print(f"      Кол-во продаж: {int(row['count'])}")
        
        # 4. Анализ по городам
        city_col = None
        for col in ['Город', 'City', 'город']:
            if col in self.df.columns:
                city_col = col
                break
        
        if city_col and revenue_col:
            print(f"\n🌍 ТОП-5 ГОРОДОВ:")
            top_cities = self.df.groupby(city_col)[revenue_col].sum().nlargest(5)
            
            for i, (city, revenue) in enumerate(top_cities.items(), 1):
                print(f"   {i}. {city}: {revenue:,.2f} ₽")
        
        # 5. Анализ по менеджерам
        manager_col = None
        for col in ['Менеджер', 'Manager', 'менеджер', 'Salesperson']:
            if col in self.df.columns:
                manager_col = col
                break
        
        if manager_col and revenue_col:
            print(f"\n👥 ТОП МЕНЕДЖЕРОВ:")
            top_managers = self.df.groupby(manager_col)[revenue_col].agg([
                'sum', 'count'
            ]).sort_values('sum', ascending=False)
            
            for i, (manager, row) in enumerate(top_managers.iterrows(), 1):
                print(f"   {i}. {manager}: {row['sum']:,.2f} ₽ ({int(row['count'])} продаж)")
        
        # 6. Динамика по датам
        date_col = None
        for col in ['Дата', 'Date', 'дата', 'Дата_время', 'Datetime']:
            if col in self.df.columns:
                date_col = col
                break
        
        if date_col and revenue_col:
            print(f"\n📅 ДИНАМИКА ПРОДАЖ:")
            
            # Группировка по месяцам
            self.df[date_col] = pd.to_datetime(self.df[date_col], errors='coerce')
            monthly_sales = self.df.groupby(self.df[date_col].dt.to_period('M'))[revenue_col].sum()
            
            for period, sales in monthly_sales.items():
                print(f"   {period}: {sales:,.2f} ₽")
            
            # Рост/падение
            if len(monthly_sales) > 1:
                growth = ((monthly_sales.iloc[-1] - monthly_sales.iloc[0]) / monthly_sales.iloc[0]) * 100
                print(f"\n   📈 Рост за период: {growth:+.1f}%")
        
        # 7. Статусы заказов
        status_col = None
        for col in ['Статус', 'Status', 'статус']:
            if col in self.df.columns:
                status_col = col
                break
        
        if status_col:
            print(f"\n СТАТУСЫ ЗАКАЗОВ:")
            status_counts = self.df[status_col].value_counts()
            
            for status, count in status_counts.items():
                percent = (count / len(self.df)) * 100
                print(f"   {status}: {count} ({percent:.1f}%)")
        
        return True
    
    def create_visualizations(self):
        """Создание графиков"""
        print("\n" + "="*60)
        print("📈 СОЗДАНИЕ ГРАФИКОВ")
        print("="*60)
        
        if self.df is None:
            print("❌ Сначала загрузи данные!")
            return False
        
        # Настройка стиля
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
        # Поиск колонок
        date_col = next((col for col in ['Дата', 'Date', 'дата'] if col in self.df.columns), None)
        revenue_col = next((col for col in ['Выручка', 'Revenue', 'Сумма', 'Total'] if col in self.df.columns), None)
        product_col = next((col for col in ['Товар', 'Product', 'товар', 'Name'] if col in self.df.columns), None)
        category_col = next((col for col in ['Категория', 'Category', 'категория'] if col in self.df.columns), None)
        city_col = next((col for col in ['Город', 'City', 'город'] if col in self.df.columns), None)
        
        print(f"\n🔍 Найдены колонки:")
        print(f"   Дата: {date_col}")
        print(f"   Выручка: {revenue_col}")
        print(f"   Товар: {product_col}")
        print(f"   Категория: {category_col}")
        print(f"   Город: {city_col}")
        
        charts_created = 0
        
        # График 1: Динамика по датам
        if date_col and revenue_col:
            try:
                print("\n📊 Создание графика 1: Динамика...")
                self.df[date_col] = pd.to_datetime(self.df[date_col], errors='coerce')
                daily_sales = self.df.groupby(self.df[date_col].dt.date)[revenue_col].sum()
                
                plt.figure(figsize=(12, 5))
                daily_sales.plot(kind='line', marker='o', linewidth=2, markersize=4)
                plt.title('Динамика продаж по дням', fontsize=14, fontweight='bold')
                plt.xlabel('Дата', fontsize=12)
                plt.ylabel('Выручка (₽)', fontsize=12)
                plt.xticks(rotation=45, ha='right')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(f"{self.reports_dir}/01_sales_trend.png", dpi=300, bbox_inches='tight')
                plt.close()
                
                print("   ✅ Сохранён: 01_sales_trend.png")
                charts_created += 1
            except Exception as e:
                print(f"   ❌ Ошибка графика 1: {e}")
        
        # График 2: Топ товаров
        if product_col and revenue_col:
            try:
                print("\n📊 Создание графика 2: Топ товаров...")
                top_products = self.df.groupby(product_col)[revenue_col].sum().nlargest(10)
                
                plt.figure(figsize=(12, 6))
                bars = plt.bar(range(len(top_products)), top_products.values, color='steelblue', alpha=0.8)
                plt.xticks(range(len(top_products)), top_products.index, rotation=45, ha='right')
                plt.title('Топ-10 товаров по выручке', fontsize=14, fontweight='bold')
                plt.ylabel('Выручка (₽)', fontsize=12)
                plt.grid(True, alpha=0.3, axis='y')
                plt.tight_layout()
                plt.savefig(f"{self.reports_dir}/02_top_products.png", dpi=300, bbox_inches='tight')
                plt.close()
                
                print("   ✅ Сохранён: 02_top_products.png")
                charts_created += 1
            except Exception as e:
                print(f"   ❌ Ошибка графика 2: {e}")
        
        # График 3: Категории
        if category_col and revenue_col:
            try:
                print("\n📊 Создание графика 3: Категории...")
                category_sales = self.df.groupby(category_col)[revenue_col].sum()
                
                plt.figure(figsize=(10, 6))
                plt.pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%', 
                       startangle=90, colors=plt.cm.Set3.colors)
                plt.title('Распределение продаж по категориям', fontsize=14, fontweight='bold')
                plt.tight_layout()
                plt.savefig(f"{self.reports_dir}/03_categories.png", dpi=300, bbox_inches='tight')
                plt.close()
                
                print("   ✅ Сохранён: 03_categories.png")
                charts_created += 1
            except Exception as e:
                print(f"   ❌ Ошибка графика 3: {e}")
        
        # График 4: Города
        if city_col and revenue_col:
            try:
                print("\n📊 Создание графика 4: Города...")
                city_sales = self.df.groupby(city_col)[revenue_col].sum().nlargest(10)
                
                plt.figure(figsize=(12, 6))
                bars = plt.barh(range(len(city_sales)), city_sales.values, color='coral', alpha=0.8)
                plt.yticks(range(len(city_sales)), city_sales.index)
                plt.title('Топ-10 городов по выручке', fontsize=14, fontweight='bold')
                plt.xlabel('Выручка (₽)', fontsize=12)
                plt.grid(True, alpha=0.3, axis='x')
                plt.tight_layout()
                plt.savefig(f"{self.reports_dir}/04_top_cities.png", dpi=300, bbox_inches='tight')
                plt.close()
                
                print("   ✅ Сохранён: 04_top_cities.png")
                charts_created += 1
            except Exception as e:
                print(f"   ❌ Ошибка графика 4: {e}")
        
        # График 5: Гистограмма распределения
        if revenue_col:
            try:
                print("\n📊 Создание графика 5: Распределение чеков...")
                
                plt.figure(figsize=(10, 6))
                plt.hist(self.df[revenue_col].dropna(), bins=30, edgecolor='black', alpha=0.7, color='skyblue')
                plt.title('Распределение сумм чеков', fontsize=14, fontweight='bold')
                plt.xlabel('Сумма чека (₽)', fontsize=12)
                plt.ylabel('Частота', fontsize=12)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(f"{self.reports_dir}/05_distribution.png", dpi=300, bbox_inches='tight')
                plt.close()
                
                print("   ✅ Сохранён: 05_distribution.png")
                charts_created += 1
            except Exception as e:
                print(f"   ❌ Ошибка графика 5: {e}")
        
        print(f"\n✅ Всего создано графиков: {charts_created}")
        return charts_created > 0
    
    def export_to_excel(self, output_name=None):
        """Экспорт в Excel с расширенной статистикой"""
        print("\n" + "="*60)
        print("💾 ЭКСПОРТ В EXCEL")
        print("="*60)
        
        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"report_{timestamp}.xlsx"
        
        output_path = f"{self.reports_dir}/{output_name}"
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Лист 1: Основные данные
            self.df.to_excel(writer, sheet_name='Данные', index=False)
            
            # Лист 2: Сводка
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            
            summary_data = []
            for col in numeric_cols[:10]:  # Первые 10 числовых колонок
                summary_data.append({
                    'Колонка': col,
                    'Сумма': self.df[col].sum(),
                    'Среднее': self.df[col].mean(),
                    'Медиана': self.df[col].median(),
                    'Мин': self.df[col].min(),
                    'Макс': self.df[col].max(),
                    'Стд.отклонение': self.df[col].std(),
                    'Кол-во': self.df[col].count()
                })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Сводка', index=False)
            
            # Лист 3: По категориям
            category_col = next((col for col in ['Категория', 'Category'] if col in self.df.columns), None)
            revenue_col = next((col for col in ['Выручка', 'Revenue', 'Сумма'] if col in self.df.columns), None)
            
            if category_col and revenue_col:
                category_stats = self.df.groupby(category_col)[revenue_col].agg([
                    'sum', 'mean', 'median', 'count', 'min', 'max'
                ]).round(2)
                category_stats.columns = ['Сумма', 'Среднее', 'Медиана', 'Кол-во', 'Мин', 'Макс']
                category_stats.to_excel(writer, sheet_name='По категориям')
            
            # Лист 4: По городам
            city_col = next((col for col in ['Город', 'City'] if col in self.df.columns), None)
            if city_col and revenue_col:
                city_stats = self.df.groupby(city_col)[revenue_col].agg([
                    'sum', 'mean', 'count'
                ]).round(2).sort_values('sum', ascending=False)
                city_stats.columns = ['Выручка', 'Средний чек', 'Заказы']
                city_stats.to_excel(writer, sheet_name='По городам')
            
            # Лист 5: По менеджерам
            manager_col = next((col for col in ['Менеджер', 'Manager'] if col in self.df.columns), None)
            if manager_col and revenue_col:
                manager_stats = self.df.groupby(manager_col)[revenue_col].agg([
                    'sum', 'mean', 'count'
                ]).round(2).sort_values('sum', ascending=False)
                manager_stats.columns = ['Выручка', 'Средний чек', 'Заказы']
                manager_stats.to_excel(writer, sheet_name='По менеджерам')
        
        print(f"✅ Отчёт сохранён: {output_path}")
        print(f"   Листов: 5 (Данные, Сводка, По категориям, По городам, По менеджерам)")
        return output_path
    
    def generate_full_report(self, file_path):
        """Полная генерация отчёта"""
        print("\n" + "="*60)
        print("🚀 ГЕНЕРАЦИЯ ПОЛНОГО ОТЧЁТА")
        print("="*60)
        
        self.load_data(file_path)
        self.clean_data()
        self.analyze_data_advanced()
        self.create_visualizations()
        self.export_to_excel()
        
        print("\n" + "="*60)
        print("✅ ОТЧЁТ ГОТОВ!")
        print("="*60)
        print(f"📁 Папка с отчётами: {os.path.abspath(self.reports_dir)}")
        print(f"📊 Файлов создано: {len(os.listdir(self.reports_dir))}")

# Пример использования
if __name__ == "__main__":
    generator = ExcelReportGenerator()
    
    # Если есть тестовый файл
    test_file = "data/large_sales_data.xlsx"
    if os.path.exists(test_file):
        generator.generate_full_report(test_file)
    else:
        print("📝 Файл не найден. Создай данные:")
        print("   python generate_large_dataset.py")
        print("   Или используй GUI: python src/gui.py")