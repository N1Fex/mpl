import json
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from Lab2.producer import send_message


class GUIManager:

    def __init__(self, win_size: str, win_name: str):
        root = tk.Tk()
        root.title(win_name)
        root.geometry(win_size)
        root.resizable(True, True)

        tk.Label(root, text="Название таблицы:", font=("Arial", 12)).pack(pady=10)
        self.table_name_entry = tk.Entry(root, width=50, font=("Arial", 11))
        self.table_name_entry.pack()

        tk.Label(root, text="Столбцы (по одному в строке):", font=("Arial", 12)).pack(pady=(20, 5), anchor="w", padx=20)
        self.columns_frame = tk.Frame(root)
        self.columns_frame.pack(fill=tk.X, padx=20)

        self.columns_entries = []

        add_btn = tk.Button(root, text="+ Добавить столбец", command=self.add_column, bg="lightgreen")
        add_btn.pack(pady=5)

        self.add_column()

        tk.Label(root, text="Данные (JSON массив объектов):", font=("Arial", 12)).pack(pady=(20, 5), anchor="w",
                                                                                       padx=20)

        self.json_input = scrolledtext.ScrolledText(root, height=12, font=("Consolas", 10))
        self.json_input.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.json_input.insert(tk.END, '[\n    {\n        \n    }\n]')

        validate_btn = tk.Button(root, text="Добавить таблицу", command=self.send_data_to_db, bg="#4CAF50", fg="white",
                                 font=("Arial", 12, "bold"), height=2)
        validate_btn.pack(fill=tk.X, padx=20, pady=10)

        root.mainloop()

    def get_columns(self):
        columns = []
        for entry in self.columns_entries[:]:
            try:
                name = entry["name"].get().strip()
                col_type = entry["type"].get()
                if name:
                    columns.append({"name": name, "type": col_type})
            except:
                continue
        return columns

    def add_column(self):
        col_frame = tk.Frame(self.columns_frame)
        col_frame.pack(fill=tk.X, pady=2)

        name_entry = tk.Entry(col_frame, width=30, font=("Arial", 10))
        name_entry.pack(side=tk.LEFT, padx=(0, 5))

        type_var = tk.StringVar(value="VARCHAR")
        type_combo = ttk.Combobox(col_frame, textvariable=type_var, values=["VARCHAR", "INTEGER", "FLOAT"],
                                  state="readonly", width=20)
        type_combo.pack(side=tk.LEFT, padx=5)

        def remove_this_column():
            col_frame.destroy()
            self.columns_entries[:] = [e for e in self.columns_entries if e["frame"] is not col_frame]

        remove_btn = tk.Button(col_frame, text="✕", fg="red", font=("Arial", 10),
                               command=remove_this_column)
        remove_btn.pack(side=tk.RIGHT)

        self.columns_entries.append({"name": name_entry, "type": type_var, "frame": col_frame})

    def send_data_to_db(self):
        if self.validate():
            table_name = self.table_name_entry.get().strip()
            columns = self.get_columns()
            json_text = self.json_input.get("1.0", tk.END).strip()
            data = json.loads(json_text)

            send_message("events-mpl", json.dumps({
                "table_name": table_name,
                "columns": columns,
                "data": data
            }))


    def validate(self) -> bool:
        try:
            table_name = self.table_name_entry.get().strip()
            if not table_name:
                messagebox.showerror("Ошибка", "Введите название таблицы!")
                return False

            columns = self.get_columns()
            if not columns:
                messagebox.showerror("Ошибка", "Добавьте хотя бы один столбец!")
                return False

            json_text = self.json_input.get("1.0", tk.END).strip()
            if not json_text:
                messagebox.showerror("Ошибка", "Введите данные в формате JSON!")
                return False

            try:
                data = json.loads(json_text)
                if not isinstance(data, list):
                    messagebox.showerror("Ошибка", "JSON должен быть списком объектов!")
                    return False
            except json.JSONDecodeError as e:
                messagebox.showerror("Ошибка JSON", f"Некорректный JSON:\n{e}")
                return False

            column_names = [col["name"] for col in columns]
            column_types = {col["name"]: col["type"] for col in columns}

            for i, row in enumerate(data):
                if not isinstance(row, dict):
                    messagebox.showerror("Ошибка", f"Строка {i + 1}: должен быть объектом!")
                    return False

                row_keys = set(row.keys())
                expected_keys = set(column_names)

                missing = expected_keys - row_keys
                extra = row_keys - expected_keys

                if missing:
                    messagebox.showerror("Ошибка", f"Строка {i + 1}: отсутствуют поля: {', '.join(missing)}")
                    return False
                if extra:
                    messagebox.showerror("Ошибка", f"Строка {i + 1}: лишние поля: {', '.join(extra)}")
                    return False

                for col_name, value in row.items():
                    expected_type = column_types[col_name]
                    if value is None:
                        continue
                    if expected_type == "INTEGER":
                        if not isinstance(value, int):
                            messagebox.showerror("Ошибка типа",
                                                 f"Строка {i + 1}, столбец '{col_name}': ожидался INTEGER, получено {type(value).__name__}")
                            return False
                    elif expected_type == "VARCHAR":
                        if not isinstance(value, str):
                            messagebox.showerror("Ошибка типа",
                                                 f"Строка {i + 1}, столбец '{col_name}': ожидался VARHAR (строка), получено {type(value).__name__}")
                            return False
                    elif expected_type == "FLOAT":
                        if not isinstance(value, float):
                            messagebox.showerror("Ошибка типа",
                                                 f"Строка {i + 1}, столбец '{col_name}': ожидался FLOAT, получено {type(value).__name__}")
                            return False
            return True

        except Exception as e:
            messagebox.showerror("Неизвестная ошибка", str(e))
            return False
