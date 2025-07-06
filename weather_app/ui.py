import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import os
from weather import get_weather_data, get_hourly_forecast, get_additional_data

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        print("✅ App started")

        self.title("Weather App")
        self.geometry("400x700")
        self.resizable(False, False)
        self.configure(bg="#1e1e2f")

        self.city = "New York"
        self.user_name = ""

        self.load_assets()
        self.create_widgets()
        self.update_weather()
        print("✔️ App initialized successfully")
    def create_widgets(self):
        print("🔧 Creating widgets...")
        self.bg_label = tk.Label(self, image=self.bg_images["Default"])
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.title_label = tk.Label(self, text="Weather App", font=("Arial", 24, "bold"), bg="#1e1e2f", fg="white")
        self.title_label.pack(pady=20)
        self.city_label = tk.Label(self, text=self.city, font=("Arial", 18), bg="#1e1e2f", fg="white")
        self.city_label.pack(pady=10)
        self.weather_info = tk.Label(self, text="", font=("Arial", 16), bg="#1e1e2f", fg="white")
        self.weather_info.pack(pady=10)
        self.temp_label = tk.Label(self, text="", font=("Arial", 16), bg="#1e1e2f", fg="white")
        self.temp_label.pack(pady=10)
        self.humidity_label = tk.Label(self, text="", font=("Arial", 16), bg="#1e1e2f", fg="white")
        self.humidity_label.pack(pady=10)
        self.wind_label = tk.Label(self, text="", font=("Arial", 16), bg="#1e1e2f", fg="white")
        self.wind_label.pack(pady=10)
        self.update_button = tk.Button(self, text="Update Weather", command=self.update_weather, bg="#4a4e69", fg="white", font=("Arial", 14))
        self.update_button.pack(pady=20)
        self.hourly_button = tk.Button(self, text="Hourly Forecast", command=self.show_hourly_forecast, bg="#4a4e69", fg="white", font=("Arial", 14))
        self.hourly_button.pack(pady=10)
        self.additional_button = tk.Button(self, text="Additional Data", command=self.show_additional_data, bg="#4a4e69", fg="white", font=("Arial", 14))
        self.additional_button.pack(pady=10)
        self.user_name_entry = tk.Entry(self, font=("Arial", 14), bg="#4a4e69", fg="white")
        self.user_name_entry.pack(pady=10)
        self.user_name_entry.insert(0, "Enter your name")
        self.user_name_entry.bind("<Return>", self.set_user_name)
        self.user_name_entry.bind("<FocusIn>", self.clear_user_name_entry)
        self.user_name_label = tk.Label(self, text="", font=("Arial", 14), bg="#1e1e2f", fg="white")
        self.user_name_label.pack(pady=10)
        print("✔️ Widgets created successfully")
    def set_user_name(self, event):
        print("🔧 Setting user name...")
        name = self.user_name_entry.get().strip()
        if name:
            self.user_name = name
            self.user_name_label.config(text=f"Hello, {self.user_name}!")
            print(f"✔️ User name set to: {self.user_name}")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid name.")
            print("⚠️ User name input error: No name entered")
    def clear_user_name_entry(self, event):
        print("🔧 Clearing user name entry...")
        if self.user_name_entry.get() == "Enter your name":
            self.user_name_entry.delete(0, tk.END)
            print("✔️ User name entry cleared")
        else:
            print("✔️ User name entry not cleared, already contains text")
    def update_weather(self):
        print("🔄 Updating weather data...")
        weather_data = get_weather_data(self.city)
        if "error" in weather_data:
            messagebox.showerror("Error", f"Failed to fetch weather data: {weather_data['error']}")
            print(f"⚠️ Weather data fetch error: {weather_data['error']}")
            return
        self.city_label.config(text=weather_data.get("name", self.city))
        self.weather_info.config(text=weather_data.get("weather", [{}])[0].get("description", "No description available").capitalize())
        self.temp_label.config(text=f"Temperature: {weather_data.get('main', {}).get('temp', 'N/A')}°C")
        self.humidity_label.config(text=f"Humidity: {weather_data.get('main', {}).get('humidity', 'N/A')}%")
        self.wind_label.config(text=f"Wind Speed: {weather_data.get('wind', {}).get('speed', 'N/A')} m/s")
        self.update_background(weather_data.get("weather", [{}])[0].get("main", "Default"))
        print("✔️ Weather data updated successfully")
    def show_hourly_forecast(self):
        print("🔄 Fetching hourly forecast...")
        hourly_data = get_hourly_forecast(self.city)
        if "error" in hourly_data:
            messagebox.showerror("Error", f"Failed to fetch hourly forecast: {hourly_data['error']}")
            print(f"⚠️ Hourly forecast fetch error: {hourly_data['error']}")
            return  
        forecast_window = tk.Toplevel(self)
        forecast_window.title(f"Hourly Forecast for {self.city}")   
        forecast_window.geometry("400x600")
        forecast_window.configure(bg="#1e1e2f")
        forecast_window.resizable(False, False)
        forecast_label = tk.Label(forecast_window, text=f"Hourly Forecast for {self.city}", font=("Arial", 18, "bold"), bg="#1e1e2f", fg="white")
        forecast_label.pack(pady=20)
        hourly_listbox = tk.Listbox(forecast_window, font=("Arial", 14), bg="#4a4e69", fg="white")
        hourly_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        for hour in hourly_data.get("list", []):
            dt = datetime.datetime.fromtimestamp(hour["dt"])
            temp = hour["main"]["temp"]
            description = hour["weather"][0]["description"].capitalize()
            hourly_listbox.insert(tk.END, f"{dt.strftime('%Y-%m-%d %H:%M')}: {temp}°C, {description}")
        print("✔️ Hourly forecast displayed successfully")
    def show_additional_data(self):
        print("🔄 Fetching additional weather data...")
        weather_data = get_weather_data(self.city)
        if "error" in weather_data:
            messagebox.showerror("Error", f"Failed to fetch additional data: {weather_data['error']}")
            print(f"⚠️ Additional data fetch error: {weather_data['error']}")
            return
        lat = weather_data.get("coord", {}).get("lat")
        lon = weather_data.get("coord", {}).get("lon")  
        if lat is None or lon is None:
            messagebox.showerror("Error", "Could not retrieve coordinates for additional data.")
            print("⚠️ Additional data fetch error: Coordinates not found")
            return
        additional_data = get_additional_data(lat, lon)
        if "error" in additional_data:
            messagebox.showerror("Error", f"Failed to fetch additional data: {additional_data['error']}")
            print(f"⚠️ Additional data fetch error: {additional_data['error']}")
            return
        additional_window = tk.Toplevel(self)
        additional_window.title(f"Additional Data for {self.city}")
        additional_window.geometry("400x600")
        additional_window.configure(bg="#1e1e2f")
        additional_window.resizable(False, False)
        additional_label = tk.Label(additional_window, text=f"Additional Data for {self.city}", font=("Arial", 18, "bold"), bg="#1e1e2f", fg="white")
        additional_label.pack(pady=20)
        additional_info = tk.Text(additional_window, font=("Arial", 14), bg="#4a4e69", fg="white")
        additional_info.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        additional_info.insert(tk.END, f"Visibility: {additional_data.get('current', {}).get('visibility', 'N/A')} m\n")
        additional_info.insert(tk.END, f"Pressure: {additional_data.get('current', {}).get('pressure', 'N/A')} hPa\n")
        additional_info.insert(tk.END, f"UV Index: {additional_data.get('current', {}).get('uvi', 'N/A')}\n")
        additional_info.insert(tk.END, f"Cloudiness: {additional_data.get('current', {}).get('clouds', 'N/A')}%\n")
        additional_info.insert(tk.END, f"Sunrise: {datetime.datetime.fromtimestamp(additional_data.get('current', {}).get('sunrise', 0)).strftime('%Y-%m-%d %H:%M')}\n")
        additional_info.insert(tk.END, f"Sunset: {datetime.datetime.fromtimestamp(additional_data.get('current', {}).get('sunset', 0)).strftime('%Y-%m-%d %H:%M')}\n")
        print("✔️ Additional data displayed successfully")
    def update_background(self, weather_condition):
        print(f"🔄 Updating background for weather condition: {weather_condition}")
        bg_image = self.bg_images.get(weather_condition, self.bg_images["Default"])
        self.bg_label.config(image=bg_image)
        self.bg_label.image = bg_image
        print(f"✔️ Background updated to: {weather_condition}")
    def load_assets(self):
        print("🔄 Loading visual assets...")
        try:
            from PIL import Image, ImageTk
        except ImportError:
            print("❌ Pillow library is not installed. Please install it using 'pip install Pillow'.")
            raise
        if not os.path.exists("visual_assets/background"):
            print("❌ Background images directory not found. Please ensure the 'visual_assets/background' directory exists.")
            raise FileNotFoundError("Background images directory not found.")
        print("✔️ Visual assets loaded successfully")
        # Load background images 
        

    
        base_path = os.path.dirname(os.path.abspath(__file__))
        backgrounds_path = os.path.join(base_path, "visual_assets", "background")

        self.bg_images = {
            "Clear": ImageTk.PhotoImage(Image.open(os.path.join(backgrounds_path, "clear.jpeg")).resize((400, 700))),
            "Clouds": ImageTk.PhotoImage(Image.open(os.path.join(backgrounds_path, "cloudy.jpeg")).resize((400, 700))),
            "Rain": ImageTk.PhotoImage(Image.open(os.path.join(backgrounds_path, "rainy.jpeg")).resize((400, 700))),
            "Snow": ImageTk.PhotoImage(Image.open(os.path.join(backgrounds_path, "snowy.jpeg")).resize((400, 700))),
            "Default": ImageTk.PhotoImage(Image.open(os.path.join(backgrounds_path, "home.jpeg")).resize((400, 700))),
        }
        print("✔️ Background images loaded successfully")