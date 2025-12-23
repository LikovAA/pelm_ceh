import tkinter as tk
from tkinter import ttk, messagebox
import math

class PelmeniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Пельменный цех")
        self.root.geometry("1200x650")
        
        # Основной контейнер
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка весов столбцов и строк
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Пельменный цех - Расчёт оборудования", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Фрейм ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Ввод данных", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Поля ввода
        labels = [
            ("Суточная выработка готовой продукции, т:", "Qday"),
            ("Продолжительность рабочей смены, ч:", "t"),
            ("Массовая доля теста в готовой продукции, %:", "a"),
            ("Производительность пельменного автомата, т/ч:", "ppa"),
            ("Производительность тестомесильной машины, т/ч:", "ptm"),
            ("Производительность куттера, т/ч:", "pcut")
        ]
        
        self.entries = {}
        for i, (label_text, key) in enumerate(labels):
            ttk.Label(input_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(input_frame, width=20)
            entry.grid(row=i, column=1, padx=(10, 0), pady=5, sticky=(tk.W, tk.E))
            self.entries[key] = entry
        
        # Кнопка расчёта
        calculate_btn = ttk.Button(input_frame, text="Рассчитать", command=self.calculate)
        calculate_btn.grid(row=len(labels), column=0, columnspan=2, pady=(15, 0))
        
        # Фрейм вывода результатов - увеличенная высота
        output_frame = ttk.LabelFrame(main_frame, text="Результаты расчёта", padding="15")
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        
        # Текстовое поле для вывода результатов - увеличенная высота
        self.result_text = tk.Text(output_frame, height=22, width=40, 
                                  font=("Courier New", 10), wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Кнопка очистки
        clear_btn = ttk.Button(output_frame, text="Очистить результаты", command=self.clear_results)
        clear_btn.grid(row=1, column=0, pady=(10, 0))
    
    def calculate(self):
        """Выполняет расчёт и выводит результаты"""
        try:
            # Получаем значения из полей ввода
            Qday = float(self.entries['Qday'].get())
            t = float(self.entries['t'].get())
            a = float(self.entries['a'].get())
            ppa = float(self.entries['ppa'].get())
            ptm = float(self.entries['ptm'].get())
            pcut = float(self.entries['pcut'].get())
            
            # Проверка на положительные значения
            for name, value in [("Суточная выработка", Qday),
                               ("Продолжительность смены", t),
                               ("Доля теста", a),
                               ("Производительность автомата", ppa),
                               ("Производительность тестомесилки", ptm),
                               ("Производительность куттера", pcut)]:
                if value <= 0:
                    raise ValueError(f"{name} должна быть положительным числом")
            
            if a > 100 or a < 0:
                raise ValueError("Массовая доля теста должна быть от 0 до 100%")
            
            # Расчёты
            Pline = Qday / 2 / t
            n_pelm_avt = Pline / ppa
            
            Pline_testo = a * Pline / 100
            n_testo = Pline_testo / ptm
            
            Pline_farsh = (100 - a) * Pline / 100
            n_cutter = Pline_farsh / pcut
            
            # Формируем результат
            result = f"РАСЧЁТ ОБОРУДОВАНИЯ\n"
            result += "=" * 40 + "\n\n"
            result += f"Производительность технологической линии: {Pline:.3f} т/ч\n\n"
            result += f"Количество пельменных автоматов: {math.ceil(n_pelm_avt)}\n"
            result += f"  (расчётное значение: {n_pelm_avt:.2f})\n\n"
            result += f"Количество тестомесильных машин: {math.ceil(n_testo)}\n"
            result += f"  (расчётное значение: {n_testo:.2f})\n\n"
            result += f"Количество куттеров: {math.ceil(n_cutter)}\n"
            result += f"  (расчётное значение: {n_cutter:.2f})\n\n"
            result += "=" * 40 + "\n"
            result += f"Всего единиц оборудования: {math.ceil(n_pelm_avt) + math.ceil(n_testo) + math.ceil(n_cutter)}"
            
            # Выводим результат
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Некорректные данные: {str(e)}\n\nПожалуйста, введите положительные числа.")
        except ZeroDivisionError:
            messagebox.showerror("Ошибка расчёта", "Деление на ноль! Проверьте введённые значения.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def clear_results(self):
        """Очищает поле результатов"""
        self.result_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = PelmeniApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()