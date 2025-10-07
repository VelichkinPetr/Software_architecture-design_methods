import tkinter as tk
from tkinter import ttk, messagebox

from WeatherInformer.src.GUI.widget_factorys import LightThemeFactory, DarkThemeFactory, AWidgetFactory
from WeatherInformer.src.weather_model import WeatherView
from WeatherInformer.src.weather_model import WeatherData

# Главное приложение
class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Погодный информатор - WeatherAPI")
        self.root.geometry("1000x550")
        self.view = WeatherView

        self.weather_data = WeatherData()
        self.current_factory = LightThemeFactory()
        self.views = self.weather_data.get_observers()

        self.create_widgets()
        self.load_default_cities()

    def remove_view(self, view: WeatherView):
        if view in self.views:
            self.views.remove(view)
        else:
            messagebox.showinfo("Информация", f"Такого города нет!")
            return

    def create_widgets(self):
        # Главный фрейм
        main_frame = self.current_factory.create_frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Заголовок
        title_label = self.current_factory.create_label(main_frame,
                                                        text="🌤️ Погодный Информатор",
                                                        font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Панель управления
        control_frame = self.current_factory.create_frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        # Поиск города
        search_frame = self.current_factory.create_frame(control_frame)
        search_frame.pack(side=tk.LEFT, padx=10)

        self.current_factory.create_label(search_frame, text="Добавить город:", font=('Arial', 10)).pack(side=tk.LEFT)

        self.city_entry = self.current_factory.create_entry(search_frame, width=20, font=('Arial', 10))
        self.city_entry.pack(side=tk.LEFT, padx=5)

        self.city_entry.bind('<Return>', lambda e: self.add_city())

        add_button = self.current_factory.create_button(search_frame,
                                                        text="➕ Добавить",
                                                        command=self.add_city,
                                                        font=('Arial', 10))
        add_button.pack(side=tk.LEFT, padx=5)

        # Кнопки смены темы
        theme_frame = self.current_factory.create_frame(control_frame)
        theme_frame.pack(side=tk.RIGHT, padx=10)

        light_theme_btn = self.current_factory.create_button(theme_frame,
                                                             text="🌞 Светлая",
                                                             command=self.set_light_theme,
                                                             font=('Arial', 9))
        light_theme_btn.pack(side=tk.LEFT, padx=2)

        dark_theme_btn = self.current_factory.create_button(theme_frame,
                                                            text="🌙 Тёмная",
                                                            command=self.set_dark_theme,
                                                            font=('Arial', 9))
        dark_theme_btn.pack(side=tk.LEFT, padx=2)

        # Фрейм для отображения погоды с прокруткой
        container_frame = self.current_factory.create_frame(main_frame)
        container_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем Canvas и Scrollbar для прокрутки
        canvas = tk.Canvas(container_frame, bg=self.current_factory.create_frame(container_frame).cget('bg'))
        scrollbar = ttk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)

        self.weather_frame = self.current_factory.create_frame(canvas)
        self.weather_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.weather_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        # Настройка прокрутки колесиком мыши
        def _on_mousewheel(event):
            canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)

    def add_city(self):
        city = self.city_entry.get().strip()
        if city:
            # Проверяем, нет ли уже такого города
            for view in self.views:
                if view.city.lower() == city.lower():
                    messagebox.showinfo("Информация", f"Город {city} уже добавлен")
                    return

            self.create_weather_view(city)
            self.weather_data.fetch_weather_data(city)
            self.city_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Предупреждение", "Введите название города")

    def create_weather_view(self, city: str):
        view = self.view(self.weather_frame, city, self.weather_data, self.current_factory)
        view.frame.pack(fill=tk.X, padx=5, pady=5, side= tk.LEFT)


    def load_default_cities(self):
        default_cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Лондон", "Нью-Йорк"]
        for city in default_cities:
            self.create_weather_view(city)
            # Задержка между запросами чтобы не превысить лимиты API
            self.root.after(500 * default_cities.index(city),
                            lambda c=city: self.weather_data.fetch_weather_data(c))

    def set_light_theme(self):
        self.change_theme(LightThemeFactory())

    def set_dark_theme(self):
        self.change_theme(DarkThemeFactory())

    def change_theme(self, factory: AWidgetFactory):
        self.current_factory = factory

        # Сохраняем текущие города
        current_cities = [view.city for view in self.views]

        # Удаляем старые вьюхи
        for view in self.views:
            view.destroy()

        self.views.clear()

        # Очищаем основной интерфейс
        for widget in self.root.winfo_children():
            widget.destroy()

        # Пересоздаем интерфейс
        self.create_widgets()

        # Восстанавливаем города с новой темой
        for city in current_cities:
            self.create_weather_view(city)

    def run(self):
        self.root.mainloop()


