import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Настройки темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ExcelReportGeneratorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(" Excel Report Generator")
        self.geometry("800x700")
        
        self.file_path = None
        self.df = None
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        title = ctk.CTkLabel(
            self, 
            text="📊 Excel Report Generator", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=15)
        
        subtitle = ctk.CTkLabel(
            self, 
            text="Автоматическая генерация отчётов из Excel/CSV", 
            font=ctk.CTkFont(size=13)
        )
        subtitle.pack(pady=(0, 20))
        
        # Фрейм выбора файла
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            file_frame, 
            text="📁 Выбор файла:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.file_label = ctk.CTkLabel(
            file_frame, 
            text="Файл не выбран", 
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.file_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        self.select_btn = ctk.CTkButton(
            file_frame, 
            text="Выбрать файл", 
            command=self.select_file,
            width=200
        )
        self.select_btn.pack(padx=15, pady=(0, 15))
        
        # Фрейм анализа
        analysis_frame = ctk.CTkFrame(self)
        analysis_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            analysis_frame, 
            text="️ Настройки:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.clean_var = tk.BooleanVar(value=True)
        self.charts_var = tk.BooleanVar(value=True)
        self.export_var = tk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(
            analysis_frame, 
            text="Очистить данные (удалить дубликаты)", 
            variable=self.clean_var
        ).pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkCheckBox(
            analysis_frame, 
            text="Создать графики", 
            variable=self.charts_var
        ).pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkCheckBox(
            analysis_frame, 
            text="Экспортировать в Excel", 
            variable=self.export_var
        ).pack(anchor="w", padx=15, pady=5)
        
        # Кнопка генерации
        self.generate_btn = ctk.CTkButton(
            self, 
            text="🚀 Сгенерировать отчёт", 
            command=self.generate_report,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.generate_btn.pack(pady=20)
        
        # Статус
        self.status_label = ctk.CTkLabel(
            self, 
            text="Готов к работе ✅", 
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(10, 5))
        
        # Прогресс
        self.progress = ctk.CTkProgressBar(self, width=700)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Лог
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(
            log_frame, 
            text="📋 Лог процесса:", 
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(
            log_frame, 
            width=700, 
            height=150, 
            font=ctk.CTkFont(size=10)
        )
        self.log_text.pack(padx=15, pady=(0, 15), fill="both", expand=True)
        self.log_text.configure(state="disabled")
        
        # Кнопка открытия папки
        self.open_btn = ctk.CTkButton(
            self, 
            text="📂 Открыть папку с отчётами", 
            command=self.open_reports_folder,
            state="disabled",
            width=250
        )
        self.open_btn.pack(pady=(0, 15))
    
    def log(self, message):
        """Добавление сообщения в лог"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.update()
    
    def select_file(self):
        """Выбор файла"""
        filetypes = [
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        
        self.file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=filetypes
        )
        
        if self.file_path:
            self.file_label.configure(
                text=self.file_path, 
                text_color="white"
            )
            self.log(f"✅ Выбран файл: {os.path.basename(self.file_path)}")
    
    def load_data(self):
        """Загрузка данных"""
        self.log(f"📂 Загрузка файла...")
        
        if self.file_path.endswith('.csv'):
            self.df = pd.read_csv(self.file_path, encoding='utf-8')
        elif self.file_path.endswith('.xlsx'):
            self.df = pd.read_excel(self.file_path)
        else:
            raise ValueError("Неподдерживаемый формат файла")
        
        self.log(f"✅ Загружено {len(self.df)} строк, {len(self.df.columns)} столбцов")
        return self.df
    
    def clean_data(self):
        """Очистка данных"""
        if not self.clean_var.get():
            self.log("⏭ Очистка пропущена")
            return
        
        self.log(" Очистка данных...")
        
        # Удаление дубликатов
        duplicates = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates()
        self.log(f"   Удалено дубликатов: {duplicates}")
        
        # Заполнение пропусков
        missing = self.df.isnull().sum().sum()
        self.df = self.df.fillna(0)
        self.log(f"   Заполнено пропусков: {missing}")
    
    def analyze_data(self):
        """Анализ данных"""
        self.log("\n📊 Анализ данных...")
        
        # Поиск числовых колонок
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) > 0:
            # Создание колонки Выручка если есть 2+ числовых колонки
            if len(numeric_cols) >= 2:
                self.df['Выручка'] = self.df[numeric_cols[0]] * self.df[numeric_cols[1]]
                total = self.df['Выручка'].sum()
                avg = self.df['Выручка'].mean()
            else:
                total = self.df[numeric_cols[0]].sum()
                avg = self.df[numeric_cols[0]].mean()
            
            self.log(f"💰 Общая сумма: {total:,.2f}")
            self.log(f"📊 Среднее значение: {avg:,.2f}")
            self.log(f"📦 Всего записей: {len(self.df)}")
        
        # Поиск текстовых колонок для группировки
        text_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(text_cols) > 0:
            self.log("\n📋 Текстовые колонки для анализа:")
            for col in text_cols[:5]:  # Первые 5
                unique_vals = self.df[col].nunique()
                self.log(f"   • {col}: {unique_vals} уникальных значений")
    
    def create_charts(self):
        """Создание графиков"""
        if not self.charts_var.get():
            self.log("⏭ Графики пропущены")
            return
        
        self.log("\n📈 Создание графиков...")
        
        sns.set_style("whitegrid")
        
        # График 1: Распределение числовых данных
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) > 0:
            plt.figure(figsize=(10, 5))
            col_name = numeric_cols[0]
            
            plt.hist(self.df[col_name].dropna(), bins=30, edgecolor='black', alpha=0.7)
            plt.title(f'Распределение: {col_name}')
            plt.xlabel(col_name)
            plt.ylabel('Частота')
            plt.tight_layout()
            plt.savefig(f"{self.reports_dir}/01_distribution.png", dpi=300)
            plt.close()
            
            self.log("   ✅ Сохранён: 01_distribution.png")
        
        # График 2: Топ категорий
        text_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(text_cols) > 0:
            plt.figure(figsize=(10, 5))
            col_name = text_cols[0]
            
            top_values = self.df[col_name].value_counts().head(10)
            top_values.plot(kind='bar', color='steelblue')
            
            plt.title(f'Топ-10: {col_name}')
            plt.xlabel(col_name)
            plt.ylabel('Количество')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(f"{self.reports_dir}/02_top_categories.png", dpi=300)
            plt.close()
            
            self.log("   ✅ Сохранён: 02_top_categories.png")
        
        self.log("✅ Все графики сохранены!")
    
    def export_excel(self):
        """Экспорт в Excel"""
        if not self.export_var.get():
            self.log("⏭ Экспорт пропущен")
            return
        
        self.log("\n💾 Экспорт в Excel...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"report_{timestamp}.xlsx"
        output_path = f"{self.reports_dir}/{output_name}"
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name='Данные', index=False)
            
            # Сводка
            summary_data = []
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            
            for col in numeric_cols[:5]:
                summary_data.append([
                    col,
                    self.df[col].sum(),
                    self.df[col].mean(),
                    self.df[col].min(),
                    self.df[col].max()
                ])
            
            if summary_data:
                summary_df = pd.DataFrame(
                    summary_data, 
                    columns=['Колонка', 'Сумма', 'Среднее', 'Мин', 'Макс']
                )
                summary_df.to_excel(writer, sheet_name='Сводка', index=False)
        
        self.log(f"✅ Отчёт сохранён: {output_path}")
        return output_path
    
    def generate_report(self):
        """Генерация отчёта"""
        if not self.file_path:
            messagebox.showwarning("Внимание", "Сначала выберите файл!")
            return
        
        try:
            self.generate_btn.configure(state="disabled", text=" Генерация...")
            self.progress.set(0)
            self.log_text.delete("1.0", "end")
            
            self.log("="*50)
            self.log(" НАЧАЛО ГЕНЕРАЦИИ ОТЧЁТА")
            self.log("="*50)
            
            # Загрузка
            self.progress.set(0.1)
            self.load_data()
            
            # Очистка
            self.progress.set(0.3)
            self.clean_data()
            
            # Анализ
            self.progress.set(0.5)
            self.analyze_data()
            
            # Графики
            self.progress.set(0.7)
            self.create_charts()
            
            # Экспорт
            self.progress.set(0.9)
            self.export_excel()
            
            # Готово
            self.progress.set(1.0)
            self.log("\n" + "="*50)
            self.log("✅ ОТЧЁТ УСПЕШНО СОЗДАН!")
            self.log("="*50)
            
            self.status_label.configure(text="Готово! ✅")
            self.open_btn.configure(state="normal")
            
            messagebox.showinfo(
                "Успех!", 
                f"Отчёт создан!\n\nПапка: {os.path.abspath(self.reports_dir)}"
            )
            
        except Exception as e:
            self.log(f"\n❌ Ошибка: {e}")
            messagebox.showerror("Ошибка", f"Не удалось создать отчёт:\n\n{e}")
        
        finally:
            self.generate_btn.configure(state="normal", text="🚀 Сгенерировать отчёт")
    
    def open_reports_folder(self):
        """Открытие папки с отчётами"""
        os.startfile(os.path.abspath(self.reports_dir))

if __name__ == "__main__":
    app = ExcelReportGeneratorGUI()
    app.mainloop()