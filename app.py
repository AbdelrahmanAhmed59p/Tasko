from customtkinter import *
from pages import TasksPage, SettingsPage

class App(CTk):
    def __init__(self):
        """إعداد التطبيق الرئيسي"""
        super().__init__()
        set_appearance_mode("light")
        self.title("TASKO")
        self.geometry("700x800")

        self.pages = {}  # تخزين الصفحات
        self.create_navbar()
        self.create_pages()

    def create_navbar(self):
        """إنشاء شريط التنقل العلوي"""
        self.navbar = CTkFrame(self, height=70, corner_radius=10)
        self.navbar.pack(side=TOP, fill=X, padx=15, pady=10, ipadx=10, ipady=10)

        CTkLabel(self.navbar, text="TASKO", font=("Arial", 26, "bold")).pack(side=LEFT, padx=15)

        buttons = [
            ("Tasks", "#0078D7", "#005A9E", "tasks"),
            ("Settings", "#FF5722", "#E64A19", "settings")
        ]

        for text, color, hover_color, page in buttons:
            self.create_nav_button(text, color, hover_color, page)

    def create_nav_button(self, text, color, hover_color, page_name):
        """إنشاء زر تنقل"""
        CTkButton(
            self.navbar, text=text, font=("Arial", 18, "bold"),
            width=130, height=50, fg_color=color, hover_color=hover_color,
            command=lambda: self.show_page(page_name)
        ).pack(side=RIGHT, padx=5)

    def create_pages(self):
        """إنشاء الصفحات الرئيسية داخل التطبيق"""
        self.container = CTkFrame(self)
        self.container.pack(fill=BOTH, expand=True, padx=15, pady=15)

        self.pages = {
            "tasks": TasksPage(self.container),
            "settings": SettingsPage(self.container)
        }

        self.show_page("tasks")

    def show_page(self, page_name):
        """إظهار الصفحة المطلوبة وإخفاء البقية"""
        for page in self.pages.values():
            page.pack_forget()

        self.pages[page_name].pack(fill="both", expand=True, padx=10, pady=10)