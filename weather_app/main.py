import tkinter as tk
from ui import WeatherUI
from weather import get_weather_data  # ← make sure this exists

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.ui = WeatherUI(root, self)
        self.ui.setup_ui()
    
    def on_city_search(self, city):
        print(f"🔍 Searching weather for: {city}")
        weather_data = get_weather_data(city)
        print("📦 Received weather data:", weather_data)
        self.ui.update_weather_display(weather_data)
    
    def on_save_journal(self, mood, notes):
        print(f"💾 Save journal with mood={mood} and notes={notes}")
    
    def on_journal_update(self, mood, notes):
        pass
    
    def toggle_dark_mode(self):
        print("🌓 Toggle theme")
        self.ui.toggle_theme()
    
    def format_time(self, timestamp):
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime("%H:%M")
    
    class config:
        @staticmethod
        def get_mood_options():
            return ["Happy", "Sad", "Anxious", "Calm", "Frustrated"]

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weather App")
    app = WeatherApp(root)
    root.mainloop()
