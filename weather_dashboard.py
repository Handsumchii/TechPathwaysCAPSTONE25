# weather_app/weather_dashboard.py

import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Text, Scrollbar
from features.weather_journal import add_journal_entry, load_journal_entries
from datetime import datetime
from weather import get_weather_data  # You must already have this working

class WeatherDashboard:
    def __init__(self, root, name, location):
        self.root = root
        self.name = name
        self.location = location
        self.root.title(f"{self.name}'s Weather Dashboard - {self.location}")

        # Header
        self.header = tk.Label(root, text=f"Welcome, {name}! 📍 {location}", font=("Arial", 16, "bold"))
        self.header.pack(pady=10)

        # Weather display (placeholder — update with your actual logic)
        self.weather_info = tk.Label(root, text="", font=("Arial", 12))
        self.weather_info.pack(pady=10)
        self.update_weather()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="➕ Add Journal Entry", command=self.prompt_journal_entry).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="📖 View Journal", command=self.view_journal_entries).pack(side=tk.LEFT, padx=10)

    def update_weather(self):
        try:
            data = get_weather_data(self.location)
            if data:
                self.current_summary = f"{data['main']['temp']}°F, {data['weather'][0]['description'].title()}"
                self.weather_info.config(text=f"Current Weather: {self.current_summary}")
            else:
                self.weather_info.config(text="Weather data not available.")
        except Exception as e:
            self.weather_info.config(text="Failed to load weather.")
            print(e)

    def prompt_journal_entry(self):
        mood = simpledialog.askstring("Mood", "How are you feeling today?")
        notes = simpledialog.askstring("Notes", "Any thoughts or experiences you want to log?")
        if mood or notes:
            date = datetime.now().strftime("%Y-%m-%d")
            add_journal_entry(date, self.location, mood, notes, self.current_summary)
            messagebox.showinfo("Saved", "Journal entry saved!")

    def view_journal_entries(self):
        entries = load_journal_entries()
        if not entries:
            messagebox.showinfo("No Entries", "No journal entries found.")
            return

        top = Toplevel(self.root)
        top.title("Weather Journal")

        text_area = Text(top, wrap="word", width=80, height=20)
        text_area.pack(side="left", fill="both", expand=True)

        scroll = Scrollbar(top, command=text_area.yview)
        scroll.pack(side="right", fill="y")
        text_area.config(yscrollcommand=scroll.set)

        for entry in entries:
            date, loc, mood, note, summary = entry
            text_area.insert("end", f"{date} - {loc}\nMood: {mood}\nNotes: {note}\nWeather: {summary}\n{'-'*60}\n")
        text_area.config(state="disabled")
        top.geometry("600x400")
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    app = WeatherDashboard(root, "User", "New York")  # Replace with actual user name and location
    root.mainloop()
# This is the main entry point for the weather dashboard application.
# It initializes the Tkinter root window and starts the WeatherDashboard with a sample user name and location.
# You can replace "User" and "New York" with actual user input or data.
# Ensure you have the necessary imports and that the weather module is correctly set up.
# The dashboard allows users to view current weather, add journal entries, and view past entries.

