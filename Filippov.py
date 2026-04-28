import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("750x550")

        # Базовая база цитат (предопределенные)
        self.base_quotes = [
            {"text": "Жизнь — это то, что случается с нами, пока мы строим планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Успех — это идти от ошибки к ошибке, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "Успех"},
            {"text": "Сложнее всего начать действовать, все остальное зависит только от упорства.", "author": "Амелия Эрхарт", "theme": "Мотивация"},
            {"text": "Логика может привести вас от пункта А к пункту Б, а воображение — куда угодно.", "author": "Альберт Эйнштейн", "theme": "Наука"}
        ]
        
        self.history = self.load_history()

        # Секция генерации
        frame_top = tk.LabelFrame(root, text="Генератор", padx=10, pady=10)
        frame_top.pack(fill="x", padx=10, pady=5)

        self.lbl_quote = tk.Label(frame_top, text="Нажмите кнопку, чтобы получить цитату", wraplength=600, font=("Arial", 11, "italic"))
        self.lbl_quote.pack(pady=10)

        btn_generate = tk.Button(frame_top, text="Сгенерировать цитату", command=self.generate_quote, bg="#2196F3", fg="white")
        btn_generate.pack()

        # Секция фильтрации истории
        frame_filter = tk.LabelFrame(root, text="История и фильтрация", padx=10, pady=10)
        frame_filter.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(frame_filter, text="Фильтр по автору:").grid(row=0, column=0)
        self.ent_filter_author = tk.Entry(frame_filter)
        self.ent_filter_author.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="По теме:").grid(row=0, column=2)
        self.ent_filter_theme = tk.Entry(frame_filter)
        self.ent_filter_theme.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(frame_filter, text="Применить", command=self.update_history_table)
        btn_filter.grid(row=0, column=4, padx=5)

        # Таблица истории
        self.tree = ttk.Treeview(frame_filter, columns=("Текст", "Автор", "Тема"), show='headings')
        self.tree.heading("Текст", text="Цитата")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Тема", text="Тема")
        self.tree.grid(row=1, column=0, columnspan=5, sticky="nsew", pady=10)
        
        frame_filter.grid_rowconfigure(1, weight=1)
        frame_filter.grid_columnconfigure(1, weight=1)

        self.update_history_table()

    def generate_quote(self):
        quote = random.choice(self.base_quotes)
        self.lbl_quote.config(text=f"«{quote['text']}»\n— {quote['author']}")
        
        # Добавляем в историю
        self.history.append(quote)
        self.save_history()
        self.update_history_table()

    def update_history_table(self):
        # Очистка
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        f_author = self.ent_filter_author.get().lower()
        f_theme = self.ent_filter_theme.get().lower()

        for q in reversed(self.history): # Сначала новые
            if f_author and f_author not in q['author'].lower(): continue
            if f_theme and f_theme not in q['theme'].lower(): continue
            
            self.tree.insert("", tk.END, values=(q['text'], q['author'], q['theme']))

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
