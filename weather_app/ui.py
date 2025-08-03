import customtkinter as ctk
from tkinter import messagebox
from weather import get_weather_data
from journal_utils import save_journal_entry, load_journal_entries
from weather_dashboard import generate_charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VibeCheck: Weather Edition")
        self.geometry("900x700")
        self.resizable(False, False)
        self.user_name = ""
        self.unit = "metric"
        self.protocol("WM_DELETE_WINDOW", self.destroy)  # graceful close
        self.switch_frame(WelcomeScreen)


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

def launch_app():
    app = App()
    app.mainloop()

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Welcome to VibeCheck 😊", font=("Arial", 26)).pack(pady=20)
        ctk.CTkLabel(self, text="What's your name?").pack()
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Enter City:").pack()
        self.city_entry = ctk.CTkEntry(self)
        self.city_entry.pack(pady=10)

        ctk.CTkButton(self, text="Get Weather ☁️", command=self.check_weather).pack(pady=20)

    def check_weather(self):
        name = self.name_entry.get().strip()
        city = self.city_entry.get().strip()
        if not name or not city:
            messagebox.showerror("Missing Info", "Please enter both your name and city.")
            return

        self.master.user_name = name
        weather_data = get_weather_data(city, self.master.unit)

        if not weather_data:
            messagebox.showerror("Error", "Failed to fetch weather.")
            return

        self.master.switch_frame(lambda master: WeatherDashboardScreen(master, weather_data))

class WeatherDashboardScreen(ctk.CTkFrame):
    def __init__(self, master, weather_data):
        super().__init__(master)
        self.weather_data = weather_data
        city = weather_data.get("name", "Unknown")
        current = weather_data.get("main", {})

        ctk.CTkLabel(self, text=f"Weather for {master.user_name} in {city}", font=("Helvetica", 20)).pack(pady=5)
        ctk.CTkLabel(self, text=f"{current.get('temp', 'N/A')}° | {weather_data.get('weather', [{'description':'N/A'}])[0]['description'].title()}").pack()

        ctk.CTkButton(self, text="Write Journal 📓", command=self.open_journal_form).pack(pady=5)
        ctk.CTkButton(self, text="Toggle °C/°F", command=self.toggle_unit).pack(pady=5)
        ctk.CTkButton(self, text="View Charts 📊", command=self.show_charts).pack(pady=5)
        ctk.CTkButton(self, text="View Entries 📃", command=self.view_entries).pack(pady=5)

    def open_journal_form(self):
        self.master.switch_frame(lambda master: JournalFormScreen(master, self.weather_data))

    def toggle_unit(self):
        self.master.unit = "imperial" if self.master.unit == "metric" else "metric"
        city = self.weather_data.get("name")
        new_data = get_weather_data(city, self.master.unit)
        if new_data:
            self.master.switch_frame(lambda master: WeatherDashboardScreen(master, new_data))

    def show_charts(self):
        charts = generate_charts()
        if not charts:
            messagebox.showinfo("No Data", "No journal data to display.")
            return

        # Store the window and charts to avoid garbage collection
        self.chart_window = ctk.CTkToplevel(self)
        self.chart_window.title("Mood & Weather Charts")
        self.chart_window.geometry("900x700")

        self.chart_canvases = []  # prevent garbage collection

        for fig in charts:
            canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.pack(pady=10)
            self.chart_canvases.append(canvas)  # ⬅️ Keep reference alive


    def view_entries(self):
        entries = load_journal_entries()
        win = ctk.CTkToplevel(self)
        win.title("Journal Entries")
        text = ctk.CTkTextbox(win, width=700, height=400)
        text.pack(pady=10)
        for entry in entries:
            text.insert("end", (
                f"{entry['timestamp']} - {entry['mood']}\n"
                f"1. What impacted your mood today? {entry.get('q1', '')}\n"
                f"2. What are you grateful for? {entry.get('q2', '')}\n"
                f"3. What is one intention for tomorrow? {entry.get('q3', '')}\n"
                f"Notes: {entry['notes']}\n\n"
            ))

class JournalFormScreen(ctk.CTkFrame):
    def __init__(self, master, weather_data):
        super().__init__(master)
        self.weather_data = weather_data

        ctk.CTkLabel(self, text="How are you feeling today?", font=("Helvetica", 16)).pack(pady=10)

        self.mood_var = ctk.StringVar()
        moods = ["😊 Happy", "😐 Neutral", "😞 Sad", "😡 Angry"]
        for mood in moods:
            ctk.CTkRadioButton(self, text=mood, variable=self.mood_var, value=mood.split()[1]).pack(anchor="w")

        self.q1 = ctk.CTkEntry(self, placeholder_text="What impacted your mood today?")
        self.q1.pack(pady=5)
        self.q2 = ctk.CTkEntry(self, placeholder_text="What are you grateful for?")
        self.q2.pack(pady=5)
        self.q3 = ctk.CTkEntry(self, placeholder_text="What is one intention for tomorrow?")
        self.q3.pack(pady=5)

        ctk.CTkLabel(self, text="Any notes?").pack(pady=5)
        self.notes_entry = ctk.CTkTextbox(self, height=100)
        self.notes_entry.pack(pady=5)

        ctk.CTkButton(self, text="Save Entry 📃", command=self.save_entry).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: master.switch_frame(lambda m: WeatherDashboardScreen(m, weather_data))).pack()

    def save_entry(self):
        mood = self.mood_var.get()
        notes = self.notes_entry.get("1.0", "end").strip()
        q1 = self.q1.get().strip()
        q2 = self.q2.get().strip()
        q3 = self.q3.get().strip()
        if not mood:
            messagebox.showerror("Missing Mood", "Please select a mood.")
            return
        save_journal_entry(self.weather_data, mood, notes, q1, q2, q3)
        self.master.switch_frame(lambda master: WeatherDashboardScreen(master, self.weather_data))






