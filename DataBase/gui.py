import tkinter as tk
import json
from tkinter import ttk, messagebox, filedialog
from database import Database
from schema import Schema, Field
from custom_types import PictureFile, RealInterval
from table import Table
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("СУБД - Управління таблицями")
        self.db = Database()

        # Головне меню
        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Файл", menu=self.file_menu)
        self.file_menu.add_command(label="Зберегти базу даних", command=self.save_database)
        self.file_menu.add_command(label="Завантажити базу даних", command=self.load_database)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Вихід", command=root.quit)

        self.table_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Таблиці", menu=self.table_menu)

        self.table_menu.add_command(label="Створити таблицю", command=self.create_table_dialog)
        self.table_menu.add_command(label="Видалити таблицю", command=self.delete_table_dialog)

        # Список таблиць
        self.tables_frame = tk.Frame(root)
        self.tables_frame.pack(fill=tk.BOTH, expand=True)

        self.table_list = ttk.Treeview(self.tables_frame, columns=("name"), show="headings")
        self.table_list.heading("name", text="Ім'я таблиці")
        self.table_list.pack(fill=tk.BOTH, expand=True)

        # Кнопки керування таблицями
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X)

        self.view_table_button = tk.Button(
            self.button_frame, text="Переглянути таблицю", command=self.view_table
        )
        self.view_table_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_table_button = tk.Button(
            self.button_frame, text="Видалити таблицю", command=self.delete_table_dialog
        )
        self.delete_table_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_row_button = tk.Button(
            self.button_frame, text="Додати рядок", command=self.add_row_dialog
        )
        self.add_row_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.reorder_columns_button = tk.Button(
            self.button_frame, text="Змінити колонки", command=self.reorder_columns_dialog
        )
        self.reorder_columns_button.pack(side=tk.LEFT, padx=5, pady=5)

    def update_table_list(self):
        """Оновити список таблиць у Treeview."""
        self.table_list.delete(*self.table_list.get_children())
        for table_name in self.db.tables.keys():
            self.table_list.insert("", "end", values=(table_name,))

    def create_table_dialog(self):
        """Діалог для створення таблиці."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Створити таблицю")

        tk.Label(dialog, text="Ім'я таблиці:").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack(pady=5)

        tk.Label(dialog, text="Поля (ім'я:тип через кому):").pack(pady=5)
        schema_entry = tk.Entry(dialog)
        schema_entry.pack(pady=5)

        def create_table():
            name = name_entry.get()
            fields_raw = schema_entry.get().split(",")
            fields = []

            valid_types = {
                "int": int,
                "float": float,
                "str": str,
                "char": "char",
                "picture": PictureFile,
                "realInvl": RealInterval
            }

            for field_raw in fields_raw:
                try:
                    field_name, field_type = field_raw.split(":")
                    field_type = valid_types.get(field_type.strip())
                    if not field_type:
                        raise ValueError
                    fields.append(Field(field_name.strip(), field_type))
                except ValueError:
                    messagebox.showerror(
                        "Помилка",
                        "Невірний формат введення полів.\n"
                        "Приклад: ім'я:int, вік:float, фото:picture\n"
                        "Допустимі типи: int, float, str, complexInteger, complexReal, picture, realInvl."
                    )
                    return

            schema = Schema(fields)
            try:
                self.db.create_table(name, schema)
                self.update_table_list()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Помилка", str(e))

        tk.Button(dialog, text="Створити", command=create_table).pack(pady=10)

    def delete_table_dialog(self):
        """Діалог для видалення таблиці."""
        selected_item = self.table_list.selection()
        if not selected_item:
            messagebox.showwarning("Попередження", "Виберіть таблицю для видалення.")
            return

        table_name = self.table_list.item(selected_item[0], "values")[0]
        confirm = messagebox.askyesno("Підтвердження", f"Видалити таблицю '{table_name}'?")
        if confirm:
            self.db.delete_table(table_name)
            self.update_table_list()


    def view_table(self):
        """Перегляд вмісту вибраної таблиці."""
        selected_item = self.table_list.selection()
        if not selected_item:
            messagebox.showwarning("Попередження", "Виберіть таблицю для перегляду.")
            return

        table_name = self.table_list.item(selected_item[0], "values")[0]
        table = self.db.tables[table_name]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Таблиця: {table_name}")

        tree = ttk.Treeview(dialog, columns=[field.name for field in table.schema.fields], show="headings")
        for field in table.schema.fields:
            tree.heading(field.name, text=field.name)

        for row in table.rows:
            # Перетворення значень перед додаванням до таблиці
            values = []
            for field in table.schema.fields:
                value = row.data[field.name]
                if isinstance(value, PictureFile):
                    values.append("Зображення збережено")  # Явне представлення для PictureFile
                elif isinstance(value, RealInterval):
                    values.append(repr(value))  # Для інтервалу
                else:
                    values.append(value)
            tree.insert("", "end", values=values)

        tree.pack(fill=tk.BOTH, expand=True)

        def delete_selected_row():
            """Видалення вибраного рядка."""
            selected_row = tree.selection()
            if not selected_row:
                messagebox.showwarning("Попередження", "Виберіть рядок для видалення.")
                return
            row_index = tree.index(selected_row[0])
            table.delete_row(row_index)
            tree.delete(selected_row[0])
            messagebox.showinfo("Успіх", "Рядок успішно видалено.")

        # Кнопка "Видалити рядок"
        delete_button = tk.Button(dialog, text="Видалити рядок", command=delete_selected_row)
        delete_button.pack(pady=10)

        def on_double_click(event):
            """Обробник подвійного клацання для перегляду зображення."""
            selected_row = tree.selection()
            if not selected_row:
                return
            item = tree.item(selected_row[0])
            row_values = item["values"]
            for idx, field in enumerate(table.schema.fields):
                if field.data_type == PictureFile:
                    picture_data = table.rows[tree.index(selected_row[0])].data[field.name]
                    if isinstance(picture_data, PictureFile):
                        temp_path = "temp_image.jpg"
                        picture_data.save_to_file(temp_path)

                        img_window = tk.Toplevel(dialog)
                        img_window.title("Перегляд зображення")
                        img = Image.open(temp_path)
                        img = ImageTk.PhotoImage(img)
                        img_label = tk.Label(img_window, image=img)
                        img_label.image = img
                        img_label.pack()

        tree.bind("<Double-1>", on_double_click)

    def add_row_dialog(self):
        """Діалог для додавання рядка до таблиці."""
        selected_item = self.table_list.selection()
        if not selected_item:
            messagebox.showwarning("Попередження", "Виберіть таблицю для додавання рядка.")
            return

        table_name = self.table_list.item(selected_item[0], "values")[0]
        table = self.db.tables[table_name]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Додати рядок у таблицю: {table_name}")

        entries = {}
        picture_paths = {}

        for field in table.schema.fields:
            tk.Label(dialog, text=field.name).pack(pady=5)
            if field.data_type == PictureFile:
                # Для типу PictureFile додаємо кнопку вибору файлу
                frame = tk.Frame(dialog)
                frame.pack(pady=5)
                path_var = tk.StringVar()
                picture_paths[field.name] = path_var

                def choose_file(field_name):
                    filepath = filedialog.askopenfilename(
                        title="Виберіть зображення",
                        filetypes=[("Зображення", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
                    )
                    if filepath:
                        picture_paths[field_name].set(filepath)

                tk.Entry(frame, textvariable=path_var, state="readonly", width=40).pack(side=tk.LEFT, padx=5)
                tk.Button(frame, text="Обрати", command=lambda fn=field.name: choose_file(fn)).pack(side=tk.LEFT)
            else:
                # Для інших типів додаємо стандартне поле введення
                entry = tk.Entry(dialog)
                entry.pack(pady=5)
                entries[field.name] = entry

        def add_row():
            data = {}
            for field in table.schema.fields:
                try:
                    if field.data_type == PictureFile:
                        filepath = picture_paths[field.name].get()
                        if not filepath:
                            raise ValueError(f"Не вибрано зображення для поля '{field.name}'.")
                        data[field.name] = PictureFile(filepath)
                    else:
                        value = entries[field.name].get()
                        if field.data_type == int:
                            value = int(value)
                        elif field.data_type == float:
                            value = float(value)
                        elif field.data_type == RealInterval:
                            start, end = map(float, value.split(","))
                            value = RealInterval(start, end)
                        data[field.name] = value
                except Exception as e:
                    messagebox.showerror("Помилка", f"Невірне значення для поля '{field.name}': {e}")
                    return
            try:
                table.add_row(data)
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Помилка", str(e))

        tk.Button(dialog, text="Додати", command=add_row).pack(pady=10)

    def reorder_columns_dialog(self):
        """Діалог для перейменування та/або перестановки колонок таблиці."""
        selected_item = self.table_list.selection()
        if not selected_item:
            messagebox.showwarning("Попередження", "Виберіть таблицю для зміни колонок.")
            return

        table_name = self.table_list.item(selected_item[0], "values")[0]
        table = self.db.tables[table_name]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Змінити колонки таблиці: {table_name}")

        tk.Label(dialog, text="Введіть новий порядок колонок (через кому):").pack(pady=5)
        current_columns = ", ".join([field.name for field in table.schema.fields])
        tk.Label(dialog, text=f"Поточні колонки: {current_columns}").pack(pady=5)

        new_order_entry = tk.Entry(dialog)
        new_order_entry.pack(pady=5)

        def apply_reorder():
            new_order = [name.strip() for name in new_order_entry.get().split(",")]
            try:
                table.rename_or_reorder_columns(new_order)
                messagebox.showinfo("Успіх", "Колонки успішно змінено.")
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Помилка", str(e))

        tk.Button(dialog, text="Застосувати", command=apply_reorder).pack(pady=10)

    def save_database(self):
        """Збереження бази даних."""
        filepath = filedialog.asksaveasfilename(
            title="Зберегти базу даних",
            defaultextension=".json",
            filetypes=[("JSON файли", "*.json"), ("Усі файли", "*.*")]
        )
        if not filepath:
            return  # Користувач скасував вибір

        try:
            # Перетворення бази даних у словник
            data = {name: table.to_dict() for name, table in self.db.tables.items()}
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Успіх", f"База даних успішно збережена у файл:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти базу даних:\n{e}")

    def load_database(self):
        """Завантаження бази даних."""
        filepath = filedialog.askopenfilename(
            title="Завантажити базу даних",
            filetypes=[("JSON файли", "*.json"), ("Усі файли", "*.*")]
        )
        if not filepath:
            return  # Користувач скасував вибір

        try:
            # Завантаження бази даних з JSON файлу
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.db.tables = {name: Table.from_dict(table_data) for name, table_data in data.items()}
            self.update_table_list()
            messagebox.showinfo("Успіх", f"База даних успішно завантажена з файлу:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити базу даних:\n{e}")

def start_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

