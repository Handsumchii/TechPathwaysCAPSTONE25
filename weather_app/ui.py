import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
from weather import get_weather_data, get_hourly_forecast, get_additional_data

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("400x700")
        self.resizable(False, False)

        self.city = "London"
        self.configure(bg="#1e1e2f")

        self.icon_images = {}
        self.load_assets()
        self.create_widgets()
        self.update_weather()

    def load_assets(self):
        icons_path = "visual_assets/icons"
        backgrounds_path = "visual_assets/background"

        self.bg_images = {
            "Clear": ImageTk.PhotoImage(Image.open(f"{backgrounds_path}/clear.jpeg").resize((400, 700))),
            "Clouds": ImageTk.PhotoImage(Image.open(f"{backgrounds_path}/cloudy.jpeg").resize((400, 700))),
            "Rain": ImageTk.PhotoImage(Image.open(f"{backgrounds_path}/rainy.jpeg").resize((400, 700))),
            "Snow": ImageTk.PhotoImage(Image.open(f"{backgrounds_path}/snowy.jpeg").resize((400, 700))),
            "Default": ImageTk.PhotoImage(Image.open(f"{backgrounds_path}/home.jpeg").resize((400, 700))),
        }

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=700, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.bg_label = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_images["Default"])

        self.location_label = self.canvas.create_text(200, 30, text=self.city, font=("Helvetica", 16), fill="white")
        self.temp_label = self.canvas.create_text(200, 80, text="", font=("Helvetica", 48), fill="white")
        self.condition_label = self.canvas.create_text(200, 130, text="", font=("Helvetica", 16), fill="lightgray")

        self.wind_text = self.canvas.create_text(200, 180, text="Wind: --", font=("Helvetica", 12), fill="white")
        self.uv_text = self.canvas.create_text(200, 210, text="UV Index: --", font=("Helvetica", 12), fill="white")
        self.aqi_text = self.canvas.create_text(200, 240, text="Air Quality: --", font=("Helvetica", 12), fill="white")

        self.forecast_frame = tk.Frame(self, bg="#1e1e2f")
        self.forecast_frame.place(x=30, y=280)

    def update_weather(self):
        data = get_weather_data(self.city)
        if "error" in data or data.get("cod") != 200:
            messagebox.showerror("Error", f"Failed to fetch weather: {data.get('message', 'Unknown error')}")
            return

        temp = int(data["main"]["temp"])
        condition = data["weather"][0]["main"]
        wind = data["wind"]["speed"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        # Update background
        bg_img = self.bg_images.get(condition, self.bg_images["Default"])
        self.canvas.itemconfig(self.bg_label, image=bg_img)

        self.canvas.itemconfig(self.temp_label, text=f"{temp}°C")
        self.canvas.itemconfig(self.condition_label, text=condition)
        self.canvas.itemconfig(self.wind_text, text=f"Wind: {wind} km/h")

        # Fetch additional data
        extra = get_additional_data(lat, lon)
        if "error" not in extra:
            uv = extra["current"].get("uvi", "N/A")
            aqi = "N/A"  # Air quality placeholder
            self.canvas.itemconfig(self.uv_text, text=f"UV Index: {uv}")
            self.canvas.itemconfig(self.aqi_text, text=f"Air Quality: {aqi}")
        else:
            self.canvas.itemconfig(self.uv_text, text="UV Index: --")
            self.canvas.itemconfig(self.aqi_text, text="Air Quality: --")

        self.update_hourly_forecast()

    def update_hourly_forecast(self):
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        forecast_data = get_hourly_forecast(self.city)
        if "error" in forecast_data or forecast_data.get("cod") != "200":
            return

        for entry in forecast_data["list"][:4]:
            hour = datetime.datetime.fromtimestamp(entry["dt"]).strftime("%I %p")
            condition = entry["weather"][0]["main"]
            temp = int(entry["main"]["temp"])

            hour_frame = tk.Frame(self.forecast_frame, bg="#1e1e2f")
            hour_frame.pack(side="left", padx=10)

            tk.Label(hour_frame, text=hour, font=("Helvetica", 12), fg="white", bg="#1e1e2f").pack()
            tk.Label(hour_frame, text=condition, font=("Helvetica", 10), fg="lightgray", bg="#1e1e2f").pack()
            tk.Label(hour_frame, text=f"{temp}°", font=("Helvetica", 12), fg="white", bg="#1e1e2f").pack()
