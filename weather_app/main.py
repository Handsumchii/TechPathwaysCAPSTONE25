import tkinter as tk
from ui import WeatherUI
from weather import get_weather_data
from journal_utils import save_journal_entry


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.ui = WeatherUI(root, self)
        self.ui.setup_ui()

    def on_city_search(self, city):
        print(f"🔍 Searching weather for: {city}")
        data = get_weather_data(city)
        if data:
            self.ui.update_weather_display(data)

    def toggle_dark_mode(self):
        print("🌓 Toggling dark mode (not implemented).")

    def format_time(self, timestamp):
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime("%H:%M")

    class config:
        @staticmethod
        def get_mood_options():
            return ["Happy", "Sad", "Anxious", "Calm", "Frustrated"]

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
