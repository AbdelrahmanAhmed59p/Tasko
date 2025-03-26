import sqlite3
from customtkinter import *

class TasksPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        """ إنشاء واجهة المستخدم """
        CTkLabel(self, text="Tasks", font=("Arial", 38, "bold")).pack(pady=10)

        self.create_input_section()
        self.create_task_list()

    def create_input_section(self):
        """ إنشاء قسم إدخال المهام """
        input_frame = CTkFrame(self)
        input_frame.pack(fill="x", padx=10, pady=5)

        self.task_entry = CTkEntry(input_frame, placeholder_text="Enter a task or search...",
                                   font=("Arial", 28), height=50)
        self.task_entry.pack(fill="x", padx=5, pady=5)

        self.create_buttons(input_frame)

    def create_buttons(self, parent):
        """ إنشاء أزرار التحكم """
        buttons_frame = CTkFrame(parent)
        buttons_frame.pack(fill="x", padx=5, pady=5)

        CTkButton(buttons_frame, text="Add", font=("Arial", 24, "bold"),
                  fg_color="#4A90E2", hover_color="#357ABD", width=100,
                  command=self.add_task).pack(side="left", expand=True, padx=5, pady=5)

        CTkButton(buttons_frame, text="Search", font=("Arial", 24, "bold"),
                  fg_color="#FFA500", hover_color="#E69500", width=100,
                  command=self.search_task).pack(side="left", expand=True, padx=5, pady=5)

        CTkButton(buttons_frame, text="Show All", font=("Arial", 24, "bold"),
                  fg_color="#4CAF50", hover_color="#388E3C", width=120,
                  command=self.show_all_tasks).pack(side="left", expand=True, padx=5, pady=5)

    def create_task_list(self):
        """ إنشاء قائمة عرض المهام """
        self.tasks_frame = CTkScrollableFrame(self)
        self.tasks_frame.pack(pady=10, fill="both", expand=True, padx=10)

    def create_table(self):
        """ إنشاء جدول المهام في قاعدة البيانات """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def add_task(self):
        """ إضافة مهمة جديدة """
        task_text = self.task_entry.get().strip()
        if task_text:
            self.cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task_text, 0))
            self.conn.commit()
            self.task_entry.delete(0, "end")
            self.load_tasks()

    def load_tasks(self, search_text=""):
        """ تحميل المهام وعرضها """
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        query = "SELECT id, task, completed FROM tasks"
        params = ()
        if search_text:
            query += " WHERE task LIKE ?"
            params = (f"%{search_text}%",)

        self.cursor.execute(query, params)
        tasks = self.cursor.fetchall()

        for task_id, task_text, completed in tasks:
            self.display_task(task_id, task_text, completed)

    def display_task(self, task_id, task_text, completed):
        """ عرض المهمة في الواجهة """
        task_frame = CTkFrame(self.tasks_frame)
        task_frame.pack(pady=5, padx=10, fill="x")

        task_var = IntVar(value=completed)  
        CTkCheckBox(task_frame, text=task_text, font=("Arial", 28, "bold"),
                    height=50, variable=task_var,
                    command=lambda: self.toggle_task(task_id, task_var.get())).pack(
                    side="left", padx=5, pady=5, fill="x", expand=True)

        CTkButton(task_frame, text="Edit", width=60, fg_color="#FFC107",
                  font=("Arial", 24, "bold"), hover_color="#E0A800",
                  command=lambda: self.edit_task(task_id, task_text)).pack(side="right", padx=5)

        CTkButton(task_frame, text="X", width=60, fg_color="red",
                  font=("Arial", 28, "bold"), hover_color="#AA0000",
                  command=lambda: self.delete_task(task_id)).pack(side="right", padx=5)

    def edit_task(self, task_id, old_text):
        """ تعديل المهمة """
        edit_window = CTkToplevel(self)
        edit_window.title("Edit Task")
        edit_window.geometry("400x200")

        CTkLabel(edit_window, text="Edit Task:", font=("Arial", 24, "bold")).pack(pady=10)
        
        new_task_entry = CTkEntry(edit_window, font=("Arial", 24), height=50)
        new_task_entry.insert(0, old_text)
        new_task_entry.pack(fill="x", padx=20, pady=10)

        def save_edit():
            new_text = new_task_entry.get().strip()
            if new_text:
                self.cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_text, task_id))
                self.conn.commit()
                edit_window.destroy()
                self.load_tasks()

        CTkButton(edit_window, text="Save", font=("Arial", 24, "bold"),
                  fg_color="#4CAF50", hover_color="#388E3C", command=save_edit).pack(pady=10)

    def toggle_task(self, task_id, new_state):
        """ تحديث حالة المهمة """
        self.cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_state, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        """ حذف المهمة """
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        self.load_tasks()

    def search_task(self):
        """ البحث عن مهمة """
        search_text = self.task_entry.get().strip()
        self.task_entry.delete(0, "end")
        self.load_tasks(search_text)

    def show_all_tasks(self):
        """ عرض جميع المهام """
        self.load_tasks()

    def __del__(self):
        """ إغلاق قاعدة البيانات عند حذف الكائن """
        self.conn.close()


class SettingsPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        CTkLabel(self, text="Settings", font=("Arial", 38, "bold")).pack(pady=20)

        CTkLabel(self, text="Appearance Mode", font=("Arial", 24)).pack(anchor="w", padx=10, pady=5)
        self.mode_switch = CTkSwitch(self, text="Dark Mode", font=("Arial", 22), command=self.toggle_mode)
        self.mode_switch.pack(anchor="w", padx=10, pady=5)

    def toggle_mode(self):
        """ تبديل بين الوضع الداكن والفاتح """
        set_appearance_mode("Light" if get_appearance_mode() == "Dark" else "Dark")