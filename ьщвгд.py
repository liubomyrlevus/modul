import pandas as pd
import tkinter as tk
from tkinter.tk import Treeview
from tkinter import filedialog, messagebox
import matplotlib, pypilot as mpl

data=pd.DataFrame()
def load_data():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]) 
    if not file_path:
        return
    try:
        data = pd.read_csv(file_path)
        if not {'Назва', 'Автор', 'Рік видання', 'Жанр', 'Кількість примірників'}.issubset(data.columns):
            raise ValueError("Некоректний формат")
        data['Рік видання'] = data['Рік видання'].astype(int)
        data['Кількість примірників'] = data['Кількість примірників'].astype(int)
        update_table()
        messagebox.showinfo("Успіх")
    except Exception as e:
        messagebox.showerror("Помилка")
def save_data():
    global data
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    try:
        data.to_csv(file_path, index=False)
        messagebox.showinfo("успіх")
    except Exception as e:
        messagebox.showerror(f"Не вдалося зберегти файл {e}")
def update_table():
    global data
    for row in tree.get_children():
        tree.delete(row)
    for _, row in data.iterrows():
        tree.insert("", "end", values=(row['Назва'], row['Автор'], row['Рік видання'], row['Жанр'], row['Кількість примірників']))
def add_product():
    global data
    try:
        new_row = {
            'Назва': entry_name.get(),
            'Автор': entry_author.get(),
            'Рік видання': int(entry_year.get()),
            'Жанр': entry_zanr.get()
            'Кількість примірників': int(entry_quantity.get())
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        update_table()
    except ValueError:
        messagebox.showerror("Некоректний формат даних")
def edit_product():
    global data
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')
        idx = data[data['Назва'] == selected_values[0]].index[0]
        data.at[idx, 'Автор'] = entry_author.get()
        data.at[idx, 'Рік видання'] = entry_year.get()
        data.at[idx, 'Жанр'] = entry_zanr.get()
        data.at[idx, 'Кількість примірників'] = int(entry_quantity.get())
        update_table()
    except (IndexError, ValueError):
        messagebox.showerror("Помилка")
def delete_product():
    global data
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')
        data = data[data['Назва'] != selected_values[0]]
        update_table()
    except IndexError:
        messagebox.showerror("Помилка")
def total_quantity():
    total = data['Кількість'].sum()
    messagebox.showinfo("Загальна кількість", f"Загальна кількість товарів: {total}")
def author_value():
    result = data.groupby('Автор').apply(lambda x: (x['Кількість'] * x['Жанр']).sum())
    messagebox.showinfo("Загальна вартість",
                        "\n".join([f"{cat}: {value:.2f}" for cat, value in result.items()]))
def find_extremes():
    if data.empty:
        messagebox.showinfo("Інформація", "Немає товарів")
        return
    max_price = data.loc[data['Жанр'].idxmax()]
    max_quantity = data.loc[data['Кількість'].idxmax()]
    messagebox.showinfo(
        "Найдорожчий і найбільший товар",
        f"Найдорожчий: {max_price['Назва']} ({max_price['Жанр']} грн)\n"
        f"Найбільше на складі: {max_quantity['Назва']} ({max_quantity['Кількість']} шт)"
    )
def plot_price_quantity():
    plt.scatter(data['Кількість'], data['Жанр'])
    plt.title("Жанр від кількості")
    plt.xlabel("Кількість")
    plt.ylabel("Жанр")
    plt.show()
def plot_author_distribution():
    author_counts = data['Автор'].value_counts()
    plt.pie(author_counts, labels=author_counts.index, autopct="%1.1f%%")
    plt.title("Розподіл товарів за Авторми")
    plt.show()
def plot_price_histogram():
    plt.hist(data['Жанр'], bins=10)
    plt.title("Гістограма цін")
    plt.xlabel("Жанр")
    plt.ylabel("Кількість")
    plt.show()
def main_program():
    global tree, entry_name, entry_author, entry_quantity, entry_price
    root = tk.Tk()
    root.title("Управління товарами")
    columns = ("Назва", "Автор", "Кількість", "Жанр")
    tree = Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)
    frame = tk.Frame(root)
    frame.pack(fill=tk.X)
    entry_name = tk.Entry(frame)
    entry_author = tk.Entry(frame)
    entry_quantity = tk.Entry(frame)
    entry_price = tk.Entry(frame)
    for idx, text in enumerate(["Назва", "Автор", "Кількість", "Жанр"]):
        tk.Label(frame, text=text).grid(row=0, column=idx)
    entry_name.grid(row=1, column=0)
    entry_author.grid(row=1, column=1)
    entry_quantity.grid(row=1, column=2)
    entry_price.grid(row=1, column=3)
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill=tk.X)

    buttons = [
        ("Додати", add_product),
        ("Редагувати", edit_product),
        ("Видалити", delete_product),
        ("Загальна кількість", total_quantity),
        ("Загальна вартість", author_value),
        ("Екстремуми", find_extremes),
        ("Графік: Жанр-Кількість", plot_price_quantity),
        ("Графік: Категорії", plot_author_distribution),
        ("Гістограма цін", plot_price_histogram),
        ("Завантажити", load_data),
        ("Зберегти", save_data)
    ]
    for text, command in buttons:
        tk.Button(btn_frame, text=text, command=command).pack(side=tk.LEFT)

    root.mainloop()
