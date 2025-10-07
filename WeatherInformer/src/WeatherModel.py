import requests
import threading
from typing import Dict, Any
import tkinter as tk
from WeatherInformer.src.GUI.widget_factorys import AWidgetFactory
from WeatherInformer.src.observer import ASubject, AObserver


class WeatherData(ASubject):
    def __init__(self):
        super().__init__()
        self._weather_data = {}
        self._api_key = "4c9cd7c1a8524b7bae7132636250610"  # Замените на ваш API ключ от WeatherAPI

    def set_weather_data(self, city: str, data: Dict[str, Any]):
        self._weather_data[city] = data
        self.notify({city: data})

    def get_weather_data(self, city: str) -> Dict[str, Any]:
        return self._weather_data.get(city, {})

    def get_observers(self):
        return self._observers

    def fetch_weather_data(self, city: str):
        """Запрос данных о погоде из WeatherAPI"""

        def fetch():
            try:
                # Используем WeatherAPI
                url = f"http://api.weatherapi.com/v1/current.json?key={self._api_key}&q={city}&lang=ru"
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    current = data['current']
                    location = data['location']

                    weather_info = {
                        'city': location['name'],
                        'country': location['country'],
                        'temperature': current['temp_c'],
                        'feels_like': current['feelslike_c'],
                        'humidity': current['humidity'],
                        'pressure': current['pressure_mb'],
                        'description': current['condition']['text'],
                        'wind_speed': current['wind_kph'],
                        'wind_dir': current['wind_dir'],
                        'precipitation': current['precip_mm'],
                        'visibility': current['vis_km'],
                        'uv_index': current['uv'],
                        'icon': current['condition']['icon'],
                        'last_updated': current['last_updated']
                    }
                    self.set_weather_data(city, weather_info)
                else:
                    error_msg = self._get_error_message(response.status_code, response.json())
                    self.set_weather_data(city, {'error': error_msg})

            except requests.exceptions.RequestException as e:
                self.set_weather_data(city, {'error': f'Ошибка подключения: {str(e)}'})
            except Exception as e:
                self.set_weather_data(city, {'error': f'Произошла ошибка: {str(e)}'})

        thread = threading.Thread(target=fetch)
        thread.daemon = True
        thread.start()

    def _get_error_message(self, status_code: int, response_data: Dict) -> str:
        """Получение понятного сообщения об ошибке от WeatherAPI"""
        if status_code == 400:
            return "Неверный запрос. Проверьте название города."
        elif status_code == 401:
            return "Неверный API ключ."
        elif status_code == 403:
            return "Доступ запрещен. Проверьте ваш тарифный план."
        elif status_code == 404:
            return "Город не найден."
        else:
            error_msg = response_data.get('error', {}).get('message', 'Неизвестная ошибка')
            return f"Ошибка {status_code}: {error_msg}"


class WeatherView(AObserver):
    def __init__(self, parent, city: str, weather_data: WeatherData, factory: AWidgetFactory):
        self.parent = parent
        self.city = city
        self.weather_data = weather_data
        self.factory = factory
        self.frame = None
        self.create_widgets()

        self.weather_data.attach(self)

    def create_widgets(self):
        self.frame = self.factory.create_frame(self.parent, padx=10, pady=10)

        # Заголовок города
        self.city_label = self.factory.create_label(self.frame,
                                                    text=f"Загрузка...",
                                                    font=('Arial', 12, 'bold'))
        self.city_label.pack(pady=5)

        # Основная информация
        info_frame = self.factory.create_frame(self.frame)
        info_frame.pack(fill=tk.X, pady=5)

        # Температура
        self.temp_label = self.factory.create_label(info_frame, text="🌡 Температура: --", font=('Arial', 10))
        self.temp_label.pack(anchor='w')

        self.feels_like_label = self.factory.create_label(info_frame, text="💨 Ощущается как: --", font=('Arial', 10))
        self.feels_like_label.pack(anchor='w')

        # Погодные условия
        self.description_label = self.factory.create_label(info_frame, text="☁️ Описание: --", font=('Arial', 10))
        self.description_label.pack(anchor='w')

        # Дополнительная информация
        details_frame = self.factory.create_frame(self.frame)
        details_frame.pack(fill=tk.X, pady=5)

        self.humidity_label = self.factory.create_label(details_frame, text="💧 Влажность: --", font=('Arial', 9))
        self.humidity_label.pack(anchor='w')

        self.pressure_label = self.factory.create_label(details_frame, text="📊 Давление: --", font=('Arial', 9))
        self.pressure_label.pack(anchor='w')

        self.wind_label = self.factory.create_label(details_frame, text="🌬️ Ветер: --", font=('Arial', 9))
        self.wind_label.pack(anchor='w')

        self.precipitation_label = self.factory.create_label(details_frame, text="🌧️ Осадки: --", font=('Arial', 9))
        self.precipitation_label.pack(anchor='w')

        self.visibility_label = self.factory.create_label(details_frame, text="👁️ Видимость: --", font=('Arial', 9))
        self.visibility_label.pack(anchor='w')

        self.uv_label = self.factory.create_label(details_frame, text="☀️ UV индекс: --", font=('Arial', 9))
        self.uv_label.pack(anchor='w')

        # Время обновления
        self.update_time_label = self.factory.create_label(details_frame, text="🕒 Обновлено: --", font=('Arial', 8))
        self.update_time_label.pack(anchor='w')

        # Ошибки
        self.error_label = self.factory.create_label(self.frame, text="", fg='red', font=('Arial', 9))
        self.error_label.pack(pady=5)

        # Кнопки
        button_frame = self.factory.create_frame(self.frame)
        button_frame.pack(pady=5)

        self.update_button = self.factory.create_button(button_frame,
                                                        text="🔄 Обновить",
                                                        command=self.update_weather,
                                                        font=('Arial', 9))
        self.update_button.pack(side=tk.LEFT, padx=2)

        self.remove_button = self.factory.create_button(button_frame,
                                                        text="❌ Удалить",
                                                        command=self.remove_view,
                                                        font=('Arial', 9))
        self.remove_button.pack(side=tk.LEFT, padx=2)

    def update(self, weather_data: Dict[str, Any]):
        if self.city in weather_data:
            data = weather_data[self.city]
            if 'error' in data:
                self.show_error(data['error'])
            else:
                self.display_weather(data)

    def display_weather(self, data: Dict[str, Any]):
        self.error_label.config(text="")

        # Обновляем основную информацию
        self.city_label.config(text=f"{data['city']}, {data['country']}")
        self.temp_label.config(text=f"🌡 Температура: {data['temperature']:.1f}°C")
        self.feels_like_label.config(text=f"💨 Ощущается как: {data['feels_like']:.1f}°C")
        self.description_label.config(text=f"☁️ {data['description']}")

        # Обновляем детали
        self.humidity_label.config(text=f"💧 Влажность: {data['humidity']}%")
        self.pressure_label.config(text=f"📊 Давление: {data['pressure']} hPa")
        self.wind_label.config(text=f"🌬️ Ветер: {data['wind_speed']} км/ч, {data['wind_dir']}")
        self.precipitation_label.config(text=f"🌧️ Осадки: {data['precipitation']} мм")
        self.visibility_label.config(text=f"👁️ Видимость: {data['visibility']} км")
        self.uv_label.config(text=f"☀️ UV индекс: {data['uv_index']}")

        # Время обновления
        update_time = data['last_updated'].replace('T', ' ')
        self.update_time_label.config(text=f"🕒 Обновлено: {update_time}")

    def show_error(self, error_message: str):
        self.error_label.config(text=error_message)
        self.city_label.config(text=f"{self.city}")

        # Сбрасываем все поля
        fields = [
            self.temp_label, self.feels_like_label, self.description_label,
            self.humidity_label, self.pressure_label, self.wind_label,
            self.precipitation_label, self.visibility_label, self.uv_label,
            self.update_time_label
        ]

        for field in fields:
            current_text = field.cget('text')
            if ':' in current_text:
                field.config(text=current_text.split(':')[0] + ': --')

    def update_weather(self):
        self.weather_data.fetch_weather_data(self.city)

    def remove_view(self):
        self.destroy()

    def destroy(self):
        self.weather_data.detach(self)
        if self.frame:
            self.frame.destroy()
