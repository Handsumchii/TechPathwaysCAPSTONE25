# weather_app/main.py

import tkinter as tk
from ui import HomeScreen  # your welcome screen
from weather_dashboard import WeatherDashboard  # the full app view

def start_app(name, location):
    root = tk.Tk()
    root.geometry("800x500")
    app = WeatherDashboard(root, name, location)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    HomeScreen(root, on_continue=start_app)
    root.mainloop()
# This is the main entry point for the weather app.
# It initializes the Tkinter root window and starts the app with a welcome screen.

