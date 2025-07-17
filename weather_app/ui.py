import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from journal_utils import save_journal_entry

# 🧠 Journal categories and questions
JOURNAL_QUESTIONS = {
    "Gratitude": [
        "What are you grateful for today?",
        "Who made a positive impact on your day?",
        "What small thing made you smile?"
    ],
    "Challenges": [
        "What challenges did you face today?",
        "How did you handle those challenges?",
        "What can you learn from them?"
    ],
    "Goals": [
        "What is one goal you want to achieve?",
        "What steps will you take to reach it?",
        "How will you celebrate when you succeed?"
    ]
}

class WeatherUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.city_var = tk.StringVar(value="New York")
        self.mood_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.answer_textboxes = []
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
            self.bg_image = bg  # keep reference
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

        # Category dropdown
        categories = list(JOURNAL_QUESTIONS.keys())
        self.category_var.set(categories[0])
        ttk.Label(frame, text="Category:").pack(anchor='w', padx=5)
        dropdown = ttk.Combobox(frame, textvariable=self.category_var, values=categories, state="readonly")
        dropdown.pack(fill='x', padx=5)
        dropdown.bind("<<ComboboxSelected>>", self.on_category_change)

        # Mood dropdown
        ttk.Label(frame, text="Mood:").pack(anchor='w', padx=5, pady=(10, 0))
        mood_values = self.app.config.get_mood_options()
        ttk.Combobox(frame, textvariable=self.mood_var, values=mood_values, state="readonly").pack(fill='x', padx=5)

        # Journal question and answer area
        self.questions_frame = tk.Frame(frame)
        self.questions_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.display_questions(self.category_var.get())

        # Save button
        tk.Button(frame, text="Save Entry", command=self.save_journal).pack(pady=10)

    def display_questions(self, category):
        for widget in self.questions_frame.winfo_children():
            widget.destroy()
        self.answer_textboxes.clear()

        questions = JOURNAL_QUESTIONS.get(category, [])
        for q in questions:
            tk.Label(self.questions_frame, text=q, wraplength=600, justify='left').pack(anchor='w', pady=(10, 0))
            text_box = tk.Text(self.questions_frame, height=3, wrap=tk.WORD)
            text_box.pack(fill='x', pady=(0, 10))
            self.answer_textboxes.append(text_box)

    def on_category_change(self, event=None):
        selected_category = self.category_var.get()
        self.display_questions(selected_category)

    def save_journal(self):
        mood = self.mood_var.get()
        city = self.city_var.get()
        category = self.category_var.get()
        answers = [tb.get("1.0", tk.END).strip() for tb in self.answer_textboxes]

        if not mood or not any(answers):
            messagebox.showwarning("Incomplete", "Please select a mood and answer at least one question.")
            return

        # Build structured notes dictionary
        notes_dict = {}
        questions = JOURNAL_QUESTIONS.get(category, [])
        for q, a in zip(questions, answers):
            notes_dict[q] = a

        try:
            save_journal_entry(city=city, mood=mood, notes=notes_dict)
            messagebox.showinfo("Success", "Journal entry saved!")
            for tb in self.answer_textboxes:
                tb.delete("1.0", tk.END)
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

    def update_forecast_plot(self, forecast):
        if not forecast or not self.forecast_fig:
            return
        ax = self.forecast_fig.gca()
        ax.clear()
        hours = [f['dt_txt'].split()[1][:5] for f in forecast[:6]]
        temps = [f['main']['temp'] for f in forecast[:6]]
        ax.plot(hours, temps, marker='o')
        ax.set_title("Next 6 Hours Forecast")
        ax.set_ylabel("Temp (°C)")
        ax.set_xlabel("Time")
        self.forecast_canvas.draw()
