from ui import WeatherApp

if __name__ == "__main__":
    try:
        app = WeatherApp()
        app.mainloop()
    except Exception as e:
        print(f"App failed to run: {e}")

