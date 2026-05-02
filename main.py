import tkinter as tk
from tkinter import ttk, messagebox
import json

MOVIES_FILE = 'movies.json'

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("700x500")

        self.movies = self.load_movies()
        self.setup_ui()

    def load_movies(self):
        try:
            with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # Возвращаем пустой список при поврежденном или пустом файле
            return []

    def save_movies(self):
        with open(MOVIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)

    def setup_ui(self):
        # --- Форма ввода ---
        frame_input = ttk.LabelFrame(self.root, text="Добавление фильма", padding=10)
        frame_input.pack(padx=10, pady=10, fill='x')

        labels = ["Название:", "Жанр:", "Год выпуска:", "Рейтинг (0-10):"]
        self.entries = []

        for i, text in enumerate(labels):
            ttk.Label(frame_input, text=text).grid(row=0, column=i*2, padx=5, pady=5)
            entry = ttk.Entry(frame_input, width=15)
            entry.grid(row=0, column=i*2+1, padx=5, pady=5)
            self.entries.append(entry)

        self.entry_title, self.entry_genre, self.entry_year, self.entry_rating = self.entries

        btn_add = ttk.Button(frame_input, text="Добавить фильм", command=self.add_movie)
        btn_add.grid(row=1, column=0, columnspan=8, pady=10)

        # --- Блок фильтрации ---
        frame_filter = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        frame_filter.pack(padx=10, pady=5, fill='x')

        ttk.Label(frame_filter, text="Жанр:").grid(row=0, column=0, padx=5)
        self.entry_filter_genre = ttk.Entry(frame_filter, width=15)
        self.entry_filter_genre.grid(row=0, column=1, padx=5)

        ttk.Label(frame_filter, text="Год (мин):").grid(row=0, column=2, padx=5)
        self.entry_filter_year = ttk.Entry(frame_filter, width=10)
        self.entry_filter_year.grid(row=0, column=3, padx=5)

        btn_filter = ttk.Button(frame_filter, text="Применить", command=self.apply_filter)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_reset = ttk.Button(frame_filter, text="Сброс", command=self.reset_filter)
        btn_reset.grid(row=0, column=5, padx=5)

        # --- Таблица ---
        columns = ('title', 'genre', 'year', 'rating')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('title', text='Название')
        self.tree.heading('genre', text='Жанр')
        self.tree.heading('year', text='Год выпуска')
        self.tree.heading('rating', text='Рейтинг')

        self.tree.column('year', width=100)
        self.tree.column('rating', width=100)
        
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.refresh_list(self.movies)

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()

        if not (title and genre and year_str and rating_str):
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            year = int(year_str)
        except ValueError:
            messagebox.showwarning("Ошибка", "Год должен быть целым числом!")
            return

        try:
            rating = float(rating_str)
            if not (0.0 <= rating <= 10.0):
                raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        new_movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }

        self.movies.append(new_movie)
        self.save_movies()
        self.refresh_list(self.movies)

        # Очистка полей
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def refresh_list(self, data_to_display):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in data_to_display:
            self.tree.insert('', tk.END, values=(movie['title'], movie['genre'], movie['year'], movie['rating']))

    def apply_filter(self):
        filter_genre = self.entry_filter_genre.get().strip().lower()
        filter_year_str = self.entry_filter_year.get().strip()

        # Валидация фильтра года
        filter_year = None
        if filter_year_str:
            try:
                filter_year = int(filter_year_str)
            except ValueError:
                messagebox.showwarning("Ошибка фильтра", "Год в фильтре должен быть целым числом!")
                return

        filtered = []
        for m in self.movies:
            match_genre = (not filter_genre or filter_genre in m['genre'].lower())
            match_year = (filter_year is None or m['year'] >= filter_year)
            if match_genre and match_year:
                filtered.append(m)

        self.refresh_list(filtered)

    def reset_filter(self):
        self.entry_filter_genre.delete(0, tk.END)
        self.entry_filter_year.delete(0, tk.END)
        self.refresh_list(self.movies)


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()