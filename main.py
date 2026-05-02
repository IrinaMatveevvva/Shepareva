import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = 'expenses.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_expense():
    amount = entry_amount.get()
    category = combo_category.get()
    date = entry_date.get()

    if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
        messagebox.showerror('Ошибка', 'Сумма должна быть положительным числом')
        return

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror('Ошибка', 'Дата должна быть в формате ГГГГ-ММ-ДД')
        return

    expense = {'amount': float(amount), 'category': category, 'date': date}
    data.append(expense)
    save_data(data)
    update_table()
    clear_inputs()

def update_table(filter_category=None, filter_date=None):
    for i in tree.get_children():
        tree.delete(i)
    for expense in data:
        if filter_category and expense['category'] != filter_category:
            continue
        if filter_date and expense['date'] != filter_date:
            continue
        tree.insert('', 'end', values=(expense['date'], expense['category'], expense['amount']))

def filter_expenses():
    category = combo_filter_category.get() if combo_filter_category.get() else None
    date = entry_filter_date.get() if entry_filter_date.get() else None
    update_table(category, date)

def sum_expenses():
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()

    try:
        if start_date:
            datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror('Ошибка', 'Даты должны быть в формате ГГГГ-ММ-ДД')
        return

    total = sum(
        e['amount'] for e in data
        if (not start_date or e['date'] >= start_date)
        and (not end_date or e['date'] <= end_date)
    )
    label_sum.config(text=f'Сумма: {total:.2f} ₽')

def clear_inputs():
    entry_amount.delete(0, tk.END)
    combo_category.set('')
    entry_date.delete(0, tk.END)

# Загрузка данных
data = load_data()

# Основное окно
root = tk.Tk()
root.title('Expense Tracker')
root.geometry('800x500')

# Вкладки
tab_control = ttk.Notebook(root)
tab_main = ttk.Frame(tab_control)
tab_filter = ttk.Frame(tab_control)
tab_sum = ttk.Frame(tab_control)
tab_control.add(tab_main, text='Добавить расход')
tab_control.add(tab_filter, text='Фильтр')
tab_control.add(tab_sum, text='Сумма за период')
tab_control.pack(expand=1, fill='both')

# Вкладка "Добавить расход"
tk.Label(tab_main, text='Сумма:').grid(row=0, column=0, padx=5, pady=5)
entry_amount = tk.Entry(tab_main)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_main, text='Категория:').grid(row=1, column=0, padx=5, pady=5)
combo_category = ttk.Combobox(tab_main, values=['Еда', 'Транспорт', 'Развлечения', 'Прочее'])
combo_category.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_main, text='Дата (ГГГГ-ММ-ДД):').grid(row=2, column=0, padx=5, pady=5)
entry_date = tk.Entry(tab_main)
entry_date.grid(row=2, column=1, padx=5, pady=5)

btn_add = tk.Button(tab_main, text='Добавить расход', command=add_expense)
btn_add.grid(row=3, column=0, columnspan=2, pady=10)

# Таблица расходов
tree = ttk.Treeview(tab_main, columns=('Дата', 'Категория', 'Сумма'), show='headings')
tree.heading('Дата', text='Дата')
tree.heading('Категория', text='Категория')
tree.heading('Сумма', text='Сумма')
tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

# Вкладка "Фильтр"
tk.Label(tab_filter, text='Категория:').grid(row=0, column=0, padx=5, pady=5)
combo_filter_category = ttk.Combobox(tab_filter, values=['Все', 'Еда', 'Транспорт', 'Развлечения', 'Прочее'])
combo_filter_category.set('Все')
combo_filter_category.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_filter, text='Дата (ГГГГ-ММ-ДД):').grid(row=1, column=0, padx=5, pady=5)
entry_filter_date = tk.Entry(tab_filter)
entry_filter_date.grid(row=1, column=1, padx=5, pady=5)

btn_filter = tk.Button(tab_filter, text='Применить фильтр', command=filter_expenses)
btn_filter.grid(row=2, column=0, columnspan=2, pady=10)

# Вкладка "Сумма за период"
tk.Label(tab_sum, text='С:').grid(row=0, column=0, padx=5, pady=5)
entry_start_date = tk.Entry(tab_sum)
entry_start_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_sum, text='По:').grid(row=1, column=0, padx=5, pady=5)
entry_end_date = tk.Entry(tab_sum)
entry_end_date.grid(row=1, column=1, padx=5, pady=5)

btn_sum = tk.Button(tab_sum, text='Посчитать сумму', command=sum_expenses)
btn_sum.grid(row=2, column=0, columnspan=2, pady=10)

label_sum = tk.Label(tab_sum, text='Сумма: 0.00 ₽')
label_sum.grid(row=3, column=0, columnspan=2, pady=10)

# Заполнение таблицы при запуске
update_table()

root.mainloop()
