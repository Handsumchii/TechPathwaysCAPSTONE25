import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WeatherUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.main_frame = None
        self.city_var = tk.StringVar(value="New York")
        self.city_entry = None
        self.weather_icon = None
        self.temp_label = None
        self.location_label = None
        self.current_theme = 'light'
        self.forecast_canvas = None
        self.forecast_fig, self.forecast_ax = None, None
        self.journal_text = None
        self.mood_var = tk.StringVar()
        self.bg_label = None
        self.bg_image = None

    def setup_ui(self):
        self.root.configure(bg='#f0f0f0')
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.setup_search_section()
        self.setup_weather_section()
        self.setup_journal_section()
        self.setup_forecast_section()
        self.load_background_image()

    def setup_search_section(self):
        search_frame = ttk.Frame(self.main_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="City:").grid(row=0, column=0)
        self.city_entry = ttk.Entry(search_frame, textvariable=self.city_var)
        self.city_entry.grid(row=0, column=1)
        self.city_entry.bind('<Return>', lambda e: self.app.on_city_search(self.city_var.get()))

        ttk.Button(search_frame, text="Get Weather",
                   command=lambda: self.app.on_city_search(self.city_var.get())).grid(row=0, column=2)
        ttk.Button(search_frame, text="Toggle Dark Mode",
                   command=self.app.toggle_dark_mode).grid(row=0, column=3)

    def setup_weather_section(self):
        weather_frame = ttk.LabelFrame(self.main_frame, text="Weather")
        weather_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        self.location_label = ttk.Label(weather_frame, text="Location: --")
        self.location_label.grid(row=0, column=0, sticky=tk.W)

        self.temp_label = ttk.Label(weather_frame, text="Temperature: --")
        self.temp_label.grid(row=1, column=0, sticky=tk.W)

        self.weather_icon = ttk.Label(weather_frame, text="🌤️", font=("Arial", 40))
        self.weather_icon.grid(row=0, column=1, rowspan=2)

        # Added missing labels with placeholders
        self.pressure_label = ttk.Label(weather_frame, text="Pressure: --")
        self.pressure_label.grid(row=2, column=0, sticky=tk.W)

        self.visibility_label = ttk.Label(weather_frame, text="Visibility: --")
        self.visibility_label.grid(row=3, column=0, sticky=tk.W)

        self.sunrise_label = ttk.Label(weather_frame, text="Sunrise: --")
        self.sunrise_label.grid(row=2, column=1, sticky=tk.W)

        self.sunset_label = ttk.Label(weather_frame, text="Sunset: --")
        self.sunset_label.grid(row=3, column=1, sticky=tk.W)

    def setup_journal_section(self):
        journal_frame = ttk.LabelFrame(self.main_frame, text="Journal")
        journal_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)

        mood_combo = ttk.Combobox(journal_frame, textvariable=self.mood_var,
                                  values=self.app.config.get_mood_options(), state="readonly")
        mood_combo.grid(row=0, column=0)

        self.journal_text = tk.Text(journal_frame, height=5, width=40)
        self.journal_text.grid(row=1, column=0)

        ttk.Button(journal_frame, text="Save",
                   command=lambda: self.app.on_save_journal(self.mood_var.get(), self.journal_text.get("1.0", tk.END))).grid(row=2, column=0)

    def setup_forecast_section(self):
        forecast_frame = ttk.LabelFrame(self.main_frame, text="Forecast")
        forecast_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)

        self.forecast_fig, self.forecast_ax = plt.subplots(figsize=(4, 2))
        self.forecast_canvas = FigureCanvasTkAgg(self.forecast_fig, master=forecast_frame)
        self.forecast_canvas.get_tk_widget().grid(row=0, column=0)
        self.forecast_canvas.draw()

    def update_weather_display(self, weather_data):
        """Update the weather display with new data"""
        if not weather_data or 'main' not in weather_data:
            self.location_label.config(text="Location: --")
            self.temp_label.config(text="Temperature: --")
            if hasattr(self, 'desc_label'):
                self.desc_label.config(text="Description: --")
            if hasattr(self, 'humidity_label'):
                self.humidity_label.config(text="Humidity: --")
            if hasattr(self, 'wind_label'):
                self.wind_label.config(text="Wind: --")
            self.weather_icon.config(text="🌤️")
            self.pressure_label.config(text="Pressure: --")
            self.visibility_label.config(text="Visibility: --")
            self.sunrise_label.config(text="Sunrise: --")
            self.sunset_label.config(text="Sunset: --")
            return

        # Ensure extra labels exist
        if not hasattr(self, 'desc_label'):
            self.desc_label = ttk.Label(self.main_frame, text="Description: --")
            self.desc_label.grid(row=4, column=0, sticky=tk.W)
        if not hasattr(self, 'humidity_label'):
            self.humidity_label = ttk.Label(self.main_frame, text="Humidity: --")
            self.humidity_label.grid(row=5, column=0, sticky=tk.W)
        if not hasattr(self, 'wind_label'):
            self.wind_label = ttk.Label(self.main_frame, text="Wind: --")
            self.wind_label.grid(row=6, column=0, sticky=tk.W)

        if 'error' in weather_data:
            self.location_label.config(text="Error fetching data")
            self.temp_label.config(text="--")
            self.desc_label.config(text="--")
            self.humidity_label.config(text="--")
            self.wind_label.config(text="--")
            self.weather_icon.config(text="🌤️")
            self.pressure_label.config(text="Pressure: --")
            self.visibility_label.config(text="Visibility: --")
            self.sunrise_label.config(text="Sunrise: --")
            self.sunset_label.config(text="Sunset: --")
            return

        # Update labels with new data
        self.location_label.config(text=f"Location: {weather_data.get('name', '--')}")
        self.temp_label.config(text=f"Temperature: {weather_data.get('main', {}).get('temp', '--')} °C")
        self.desc_label.config(text=f"Description: {weather_data.get('weather', [{}])[0].get('description', '--').capitalize()}")
        self.humidity_label.config(text=f"Humidity: {weather_data.get('main', {}).get('humidity', '--')}%")
        self.wind_label.config(text=f"Wind: {weather_data.get('wind', {}).get('speed', '--')} m/s")

        # Update icon
        icon_code = weather_data.get('weather', [{}])[0].get('icon', '01d')
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', f"{icon_code}.png")
        if os.path.exists(icon_path):
            icon_img = Image.open(icon_path).resize((64, 64))
            icon_img = ImageTk.PhotoImage(icon_img)
            self.weather_icon.config(image=icon_img)
            self.weather_icon.image = icon_img
        else:
            self.weather_icon.config(text="🌤️")

        # Extra info
        self.pressure_label.config(text=f"Pressure: {weather_data.get('main', {}).get('pressure', '--')} hPa")
        visibility = weather_data.get('visibility', None)
        if visibility is not None:
            self.visibility_label.config(text=f"Visibility: {visibility / 1000:.1f} km")
        else:
            self.visibility_label.config(text="Visibility: --")

        self.sunrise_label.config(text=f"Sunrise: {self.app.format_time(weather_data.get('sys', {}).get('sunrise', 0))}")
        self.sunset_label.config(text=f"Sunset: {self.app.format_time(weather_data.get('sys', {}).get('sunset', 0))}")

    def toggle_theme(self):
        """Toggle between light and dark themes using ttk.Style"""
        style = ttk.Style()

        if self.current_theme == 'light':
            self.current_theme = 'dark'
            self.root.configure(bg='#2e2e2e')
            style.configure("TFrame", background='#2e2e2e')
            style.configure("TLabel", background='#2e2e2e', foreground='white')
            style.configure("TButton", background='#3e3e3e', foreground='white')
            style.configure("TEntry", fieldbackground='#3e3e3e', foreground='white')
            style.configure("TCombobox", fieldbackground='#3e3e3e', foreground='white')
        else:
            self.current_theme = 'light'
            self.root.configure(bg='#f0f0f0')
            style.configure("TFrame", background='#f0f0f0')
            style.configure("TLabel", background='#f0f0f0', foreground='black')
            style.configure("TButton", background='#e0e0e0', foreground='black')
            style.configure("TEntry", fieldbackground='white', foreground='black')
            style.configure("TCombobox", fieldbackground='white', foreground='black')

        if self.journal_text:
            self.journal_text.configure(
                bg='#ffffff' if self.current_theme == 'light' else '#3a3a3a',
                fg='#000000' if self.current_theme == 'light' else '#ffffff',
                insertbackground='#000000' if self.current_theme == 'light' else '#ffffff'
            )

        if self.forecast_canvas:
            self.forecast_canvas.get_tk_widget().configure(
                bg='#ffffff' if self.current_theme == 'light' else '#2e2e2e'
            )
            self.forecast_canvas.draw()

    def load_background_image(self):
        try:
            bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'background.jpg')
            self.bg_image = Image.open(bg_path)
            self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
            self.bg_image = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = ttk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")


