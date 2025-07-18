import tkinter as tk
from tkinter import ttk, messagebox
from weather import get_weather_data
from journal_utils import save_journal_entry

class WelcomeScreen(tk.Frame):
    def __init__(self, master, on_submit_name):
        super().__init__(master)
        self.on_submit_name = on_submit_name

        # Title
        tk.Label(self, text="🌤️ VibeCheck: Weather Edition",
                 font=("Helvetica", 26, "bold"), fg="#4A90E2").pack(pady=(30, 5))

        # Tagline
        tk.Label(self, text="Track the skies. Reflect the soul.",
                 font=("Helvetica", 14, "italic"), fg="#666").pack(pady=(0, 20))

        # Name input prompt
        tk.Label(self, text="Welcome! What's your name?", font=("Helvetica", 12)).pack(pady=(10, 5))
        self.name_entry = tk.Entry(self, font=("Helvetica", 12))
        self.name_entry.pack()

        # Submit button
        tk.Button(self, text="Start Vibe Check", font=("Helvetica", 12, "bold"),
                  bg="#4A90E2", fg="white", command=self.submit_name).pack(pady=20)

    def submit_name(self):
        username = self.name_entry.get().strip()
        if username:
            self.on_submit_name(username)
        else:
            messagebox.showwarning("Input Required", "Please enter your name to continue.")

class Dashboard(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username

        self.use_celsius = True  # Default temperature unit

        # Journal categories and questions
        self.category_questions = {
            "Emotional Health": [
                "How are you feeling emotionally today?",
                "What has affected your mood most?",
                "What support do you need?"
            ],
            "Physical Health": [
                "How does your body feel today?",
                "Did the weather affect your physical activity?",
                "What can you do to take care of your health?"
            ],
            "Mindfulness": [
                "What was a mindful moment you had today?",
                "How did the weather impact your awareness?",
                "What are you grateful for today?"
            ]
        }

        self.selected_category = tk.StringVar()
        self.question_labels = []
        self.question_textboxes = []

        self.create_widgets()

    def create_widgets(self):
        # Greeting
        tk.Label(self, text=f"Welcome back, {self.username}! 👋",
                 font=("Helvetica", 16, "bold"), fg="#333").pack(pady=(20, 10))

        # City input and weather display
        tk.Label(self, text="Enter City:").pack()
        self.city_entry = tk.Entry(self)
        self.city_entry.pack()

        tk.Button(self, text="Get Weather", command=self.get_weather).pack(pady=5)

        self.toggle_temp_button = tk.Button(self, text="Switch to °F", command=self.toggle_temperature_unit)
        self.toggle_temp_button.pack(pady=5)

        self.weather_display = tk.Label(self, text="", font=("Helvetica", 14))
        self.weather_display.pack(pady=10)

        # Journal Section
        tk.Label(self, text="Today's Mood:").pack()
        self.mood_entry = tk.Entry(self)
        self.mood_entry.pack(pady=5)

        tk.Label(self, text="Select Journal Category:").pack()
        self.category_dropdown = ttk.Combobox(self, textvariable=self.selected_category)
        self.category_dropdown["values"] = list(self.category_questions.keys())
        self.category_dropdown.bind("<<ComboboxSelected>>", self.on_category_change)
        self.category_dropdown.pack(pady=5)

        self.questions_frame = tk.Frame(self)
        self.questions_frame.pack(pady=10)

        tk.Label(self, text="Additional Notes:").pack()
        self.notes_entry = tk.Text(self, height=4)
        self.notes_entry.pack(pady=5)

        tk.Button(self, text="Save Entry", command=self.save_entry).pack(pady=10)

    def toggle_temperature_unit(self):
        self.use_celsius = not self.use_celsius
        new_label = "Switch to °C" if not self.use_celsius else "Switch to °F"
        self.toggle_temp_button.config(text=new_label)

        city = self.city_entry.get()
        if city:
            self.display_weather(city)

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        self.display_weather(city)

    def display_weather(self, city):
        try:
            data = get_weather_data(city)
            kelvin_temp = data["main"]["temp"]
            if self.use_celsius:
                temperature = kelvin_temp - 273.15
                unit = "°C"
            else:
                temperature = (kelvin_temp - 273.15) * 9 / 5 + 32
                unit = "°F"

            weather = data["weather"][0]["description"].capitalize()
            output = f"{city} Weather: {temperature:.1f}{unit}, {weather}"
            self.weather_display.config(text=output)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get weather data:\n{e}")

    def on_category_change(self, event=None):
        for widget in self.questions_frame.winfo_children():
            widget.destroy()

        self.question_labels.clear()
        self.question_textboxes.clear()

        selected = self.selected_category.get()
        questions = self.category_questions.get(selected, [])

        for q in questions:
            label = tk.Label(self.questions_frame, text=q)
            label.pack(anchor="w")
            textbox = tk.Text(self.questions_frame, height=2, width=60)
            textbox.pack(pady=2)
            self.question_labels.append(label)
            self.question_textboxes.append(textbox)

    def save_entry(self):
        city = self.city_entry.get()
        mood = self.mood_entry.get()
        notes = self.notes_entry.get("1.0", tk.END).strip()

        selected = self.selected_category.get()
        questions = self.category_questions.get(selected, [])
        answers = []

        for box in self.question_textboxes:
            answer = box.get("1.0", tk.END).strip()
            answers.append(answer)

        full_entry = f"Category: {selected}\n"
        for i in range(len(questions)):
            full_entry += f"{questions[i]}\n{answers[i]}\n\n"
        full_entry += f"Mood: {mood}\nAdditional Notes: {notes}"

        try:
            save_journal_entry(city, mood, full_entry)
            messagebox.showinfo("Success", "Journal entry saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entry:\n{e}")

def launch_app():
    root = tk.Tk()
    root.geometry("600x800")
    root.title("VibeCheck: Weather Edition")

    welcome_screen = WelcomeScreen(root, lambda username: start_dashboard(username, root, welcome_screen))
    welcome_screen.pack(fill="both", expand=True)

    root.mainloop()

def start_dashboard(username, root, welcome_screen):
    welcome_screen.pack_forget()
    dashboard = Dashboard(root, username)
    dashboard.pack(fill="both", expand=True)




