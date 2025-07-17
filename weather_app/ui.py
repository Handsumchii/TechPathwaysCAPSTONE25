import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from journal_utils import save_journal_entry  # ✅ FIXED import

class WeatherUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.city_var = tk.StringVar(value="New York")
        self.mood_var = tk.StringVar()
        self.forecast_fig = None
        self.forecast_canvas = None

    def setup_ui(self):
        self.root.title("Weather App")
        self.root.geometry("900x700")
        self.load_background_image()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.place(relwidth=1, relheight=1)
        self.setup_search_section()
        self.setup_weather_section()
        self.setup_journal_section()
        self.setup_forecast_section()

    def load_background_image(self):
        try:
            path = os.path.join(os.path.dirname(__file__), 'visual_assets', 'background.jpg')
            img = Image.open(path).resize((900, 700))
            img = ImageEnhance.Brightness(img).enhance(0.5)
            bg = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_image = bg  # Keep reference
        except Exception as e:
            print(f"Background load error: {e}")

    def setup_search_section(self):
        frame = tk.Frame(self.main_frame, bg="#ffffff")
        frame.pack(pady=10)

        tk.Label(frame, text="City:").pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, textvariable=self.city_var)
        entry.pack(side=tk.LEFT)
        entry.bind("<Return>", lambda e: self.app.on_city_search(self.city_var.get()))
        tk.Button(frame, text="Get Weather", command=lambda: self.app.on_city_search(self.city_var.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Toggle Dark Mode", command=self.app.toggle_dark_mode).pack(side=tk.LEFT)

    def setup_weather_section(self):
        self.weather_frame = ttk.LabelFrame(self.main_frame, text="Weather Info")
        self.weather_frame.pack(fill='x', padx=10, pady=5)

        self.labels = {}
        keys = ['Location', 'Temperature', 'Pressure', 'Visibility', 'Sunrise', 'Sunset']
        for i, key in enumerate(keys):
            lbl = tk.Label(self.weather_frame, text=f"{key}: --")
            lbl.grid(row=i//2, column=i % 2, sticky='w')
            self.labels[key] = lbl

    def setup_journal_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Journal")
        frame.pack(fill='x', padx=10, pady=5)

        ttk.Combobox(frame, textvariable=self.mood_var, values=self.app.config.get_mood_options(), state="readonly").pack()
        self.journal_text = tk.Text(frame, height=5, wrap=tk.WORD)
        self.journal_text.pack(padx=5, pady=5)
        tk.Button(frame, text="Save Entry", command=self.save_journal).pack()

    def save_journal(self):
        mood = self.mood_var.get()
        notes = self.journal_text.get("1.0", tk.END).strip()
        city = self.city_var.get()

        if not mood or not notes:
            messagebox.showwarning("Incomplete", "Please select a mood and write some notes before saving.")
            return

        try:
            save_journal_entry(city, mood, notes)  # <-- This is the call to save the entry
            messagebox.showinfo("Success", "Journal entry saved!")
            self.journal_text.delete("1.0", tk.END)  # clear text after saving
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save journal entry:\n{e}")


    def setup_forecast_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Forecast")
        frame.pack(fill='x', padx=10, pady=5)
        self.forecast_fig, ax = plt.subplots(figsize=(4, 2))
        self.forecast_canvas = FigureCanvasTkAgg(self.forecast_fig, master=frame)
        self.forecast_canvas.get_tk_widget().pack()
        self.forecast_canvas.draw()

    def update_weather_display(self, data):
        main = data.get('main', {})
        sys = data.get('sys', {})
        self.labels['Location'].config(text=f"Location: {data.get('name', '--')}")
        self.labels['Temperature'].config(text=f"Temperature: {main.get('temp', '--')} °C")
        self.labels['Pressure'].config(text=f"Pressure: {main.get('pressure', '--')} hPa")
        vis = data.get('visibility', 0)
        self.labels['Visibility'].config(text=f"Visibility: {vis / 1000:.1f} km")
        self.labels['Sunrise'].config(text=f"Sunrise: {self.app.format_time(sys.get('sunrise', 0))}")
        self.labels['Sunset'].config(text=f"Sunset: {self.app.format_time(sys.get('sunset', 0))}")
        self.update_forecast_plot(data.get('forecast', []))
        print("🌤️ Weather display updated.")

