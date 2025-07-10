import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
import os
from PIL import Image, ImageTk

class WeatherUI:
    """Handle all UI components and layouts"""
    
    def __init__(self, root, app):
        self.root = root
        self.app = app  # Reference to main app
        
        # UI components references
        self.main_frame = None
        self.weather_frame = None
        self.journal_frame = None
        self.forecast_frame = None
        
        # Weather display widgets
        self.location_label = None
        self.temp_label = None
        self.desc_label = None
        self.humidity_label = None
        self.wind_label = None
        self.weather_icon = None
        
        # Search widgets
        self.city_var = tk.StringVar(value="New York")
        self.city_entry = None
        
        # Journal widgets
        self.mood_var = tk.StringVar()
        self.journal_text = None
        
        # Forecast widgets
        self.forecast_fig = None
        self.forecast_ax = None
        self.forecast_canvas = None
        
        # Theme variables
        self.current_theme = 'light'
        
        # Background image
        self.bg_image = None
        self.bg_label = None
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Configure root window
        self.root.configure(bg='#f0f0f0')
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        
        # Setup individual sections
        self.setup_header()
        self.setup_search_section()
        self.setup_weather_section()
        self.setup_journal_section()
        self.setup_forecast_section()
        
        # Try to load background image
        self.load_background_image()
    
    def setup_header(self):
        """Setup application header"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="🌤️ Interactive Weather App", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, 
                                  text="TechPathways Capstone Project - Justice Through Code",
                                  font=("Arial", 10, "italic"))
        subtitle_label.grid(row=1, column=0)
    
    def setup_search_section(self):
        """Setup city search section"""
        search_frame = ttk.Frame(self.main_frame)
        search_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # City search
        ttk.Label(search_frame, text="City:").grid(row=0, column=0, padx=(0, 5))
        
        self.city_entry = ttk.Entry(search_frame, textvariable=self.city_var, width=25)
        self.city_entry.grid(row=0, column=1, padx=(0, 10))
        self.city_entry.bind('<Return>', lambda e: self.app.on_city_search(self.city_var.get()))
        
        # Search button
        search_btn = ttk.Button(search_frame, text="Get Weather", 
                               command=lambda: self.app.on_city_search(self.city_var.get()))
        search_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Theme toggle button
        theme_btn = ttk.Button(search_frame, text="Toggle Dark Mode", 
                              command=self.app.toggle_dark_mode)
        theme_btn.grid(row=0, column=3, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(search_frame, text="🔄 Refresh", 
                                command=lambda: self.app.on_city_search(self.city_var.get()))
        refresh_btn.grid(row=0, column=4)
    
    def setup_weather_section(self):
        """Setup current weather display section"""
        self.weather_frame = ttk.LabelFrame(self.main_frame, text="Current Weather", padding="15")
        self.weather_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Configure grid weights
        self.weather_frame.columnconfigure(0, weight=1)
        self.weather_frame.rowconfigure(5, weight=1)
        
        # Weather info labels
        self.location_label = ttk.Label(self.weather_frame, text="Location: --", 
                                       font=("Arial", 12, "bold"))
        self.location_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.temp_label = ttk.Label(self.weather_frame, text="Temperature: --", 
                                   font=("Arial", 16, "bold"))
        self.temp_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.desc_label = ttk.Label(self.weather_frame, text="Description: --", 
                                   font=("Arial", 12))
        self.desc_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.humidity_label = ttk.Label(self.weather_frame, text="Humidity: --", 
                                       font=("Arial", 10))
        self.humidity_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.wind_label = ttk.Label(self.weather_frame, text="Wind: --", 
                                   font=("Arial", 10))
        self.wind_label.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        # Weather icon area
        icon_frame = ttk.Frame(self.weather_frame)
        icon_frame.grid(row=0, column=1, rowspan=5, padx=(20, 0), sticky=(tk.N, tk.S))
        
        self.weather_icon = ttk.Label(icon_frame, text="🌤️", font=("Arial", 64))
        self.weather_icon.grid(row=0, column=0, pady=20)
        
        # Additional weather info
        info_frame = ttk.Frame(self.weather_frame)
        info_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        
        self.pressure_label = ttk.Label(info_frame, text="Pressure: --", font=("Arial", 10))
        self.pressure_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.visibility_label = ttk.Label(info_frame, text="Visibility: --", font=("Arial", 10))
        self.visibility_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.sunrise_label = ttk.Label(info_frame, text="Sunrise: --", font=("Arial", 10))
        self.sunrise_label.grid(row=0, column=1, sticky=tk.W, padx=(20, 0), pady=2)
        
        self.sunset_label = ttk.Label(info_frame, text="Sunset: --", font=("Arial", 10))
        self.sunset_label.grid(row=1, column=1, sticky=tk.W, padx=(20, 0), pady=2)
    
    def setup_journal_section(self):
        """Setup weather journal section"""
        self.journal_frame = ttk.LabelFrame(self.main_frame, text="Weather Journal", padding="15")
        self.journal_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Configure grid weights
        self.journal_frame.columnconfigure(0, weight=1)
        self.journal_frame.rowconfigure(3, weight=1)
        
        # Mood selection
        ttk.Label(self.journal_frame, text="How's the weather making you feel?").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        mood_combo = ttk.Combobox(self.journal_frame, textvariable=self.mood_var, 
                                 values=self.app.config.get_mood_options(), 
                                 state="readonly")
        mood_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Notes section
        ttk.Label(self.journal_frame, text="Notes:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text area with scrollbar
        text_frame = ttk.Frame(self.journal_frame)
        text_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.journal_text = tk.Text(text_frame, height=8, width=30, wrap=tk.WORD)
        self.journal_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        journal_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.journal_text.yview)
        journal_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.journal_text['yscrollcommand'] = journal_scrollbar.set
        self.journal_text.bind("<KeyRelease>", lambda e: self.app.on_journal_update(
            self.mood_var.get(), self.journal_text.get("1.0", tk.END).strip()))
        # Save button
        save_btn = ttk.Button(self.journal_frame, text="Save Journal",
                              command=lambda: self.app.on_save_journal(
                                  self.mood_var.get(), self.journal_text.get("1.0", tk.END).strip()))
        save_btn.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    def setup_forecast_section(self):
        """Setup weather forecast section"""
        self.forecast_frame = ttk.LabelFrame(self.main_frame, text="Weather Forecast", padding="15")
        self.forecast_frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Configure grid weights
        self.forecast_frame.columnconfigure(0, weight=1)
        self.forecast_frame.rowconfigure(0, weight=1)
        
        # Forecast plot area
        self.forecast_fig, self.forecast_ax = plt.subplots(figsize=(5, 3))
        self.forecast_ax.set_title("Hourly Forecast")
        self.forecast_ax.set_xlabel("Hour")
        self.forecast_ax.set_ylabel("Temperature (°C)")
        
        self.forecast_canvas = FigureCanvasTkinter.FigureCanvasTkAgg(self.forecast_fig, master=self.forecast_frame)
        self.forecast_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.forecast_canvas.draw()
    def load_background_image(self):
        """Load and set background image if available"""
        try:
            bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'background.jpg')
            self.bg_image = Image.open(bg_path)
            self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.ANTIALIAS)
            self.bg_image = ImageTk.PhotoImage(self.bg_image)
            
            self.bg_label = ttk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
    def update_weather_display(self, weather_data):
        """Update weather display with new data"""
        if 'error' in weather_data:
            self.location_label.config(text="Error fetching data")
            self.temp_label.config(text="--")
            self.desc_label.config(text="--")
            self.humidity_label.config(text="--")
            self.wind_label.config(text="--")
            self.weather_icon.config(text="🌤️")
            return
        
        # Update labels with new data
        self.location_label.config(text=f"Location: {weather_data.get('name', '--')}")
        self.temp_label.config(text=f"Temperature: {weather_data.get('main', {}).get('temp', '--')} °C")
        self.desc_label.config(text=f"Description: {weather_data.get('weather', [{}])[0].get('description', '--').capitalize()}")
        self.humidity_label.config(text=f"Humidity: {weather_data.get('main', {}).get('humidity', '--')}%")
        self.wind_label.config(text=f"Wind: {weather_data.get('wind', {}).get('speed', '--')} m/s")
        
        # Update weather icon
        icon_code = weather_data.get('weather', [{}])[0].get('icon', '01d')
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', f"{icon_code}.png")
        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((64, 64), Image.ANTIALIAS)
            icon_image = ImageTk.PhotoImage(icon_image)
            self.weather_icon.config(image=icon_image)
            self.weather_icon.image = icon_image
        else:
            self.weather_icon.config(text="🌤️")
        # Update additional info
        self.pressure_label.config(text=f"Pressure: {weather_data.get('main', {}).get('pressure', '--')} hPa")
        self.visibility_label.config(text=f"Visibility: {weather_data.get('visibility', '--') / 1000} km")
        sunrise = weather_data.get('sys', {}).get('sunrise', 0)
        sunset = weather_data.get('sys', {}).get('sunset', 0)
        self.sunrise_label.config(text=f"Sunrise: {self.app.format_time(sunrise)}")
        self.sunset_label.config(text=f"Sunset: {self.app.format_time(sunset)}")
    def update_forecast_display(self, forecast_data):
        """Update forecast display with new data"""
        if 'error' in forecast_data:
            self.forecast_ax.clear()
            self.forecast_ax.set_title("Error fetching forecast")
            self.forecast_canvas.draw()
            return
        
        # Clear previous plot
        self.forecast_ax.clear()
        self.forecast_ax.set_title("Hourly Forecast")
        self.forecast_ax.set_xlabel("Hour")
        self.forecast_ax.set_ylabel("Temperature (°C)")
        
        # Extract hourly data
        hours = []
        temps = []
        
        for entry in forecast_data.get('list', []):
            hours.append(entry['dt_txt'])
            temps.append(entry['main']['temp'])
        
        # Plot new data
        self.forecast_ax.plot(hours, temps, marker='o', linestyle='-', color='blue')
        self.forecast_ax.tick_params(axis='x', rotation=45)
        
        # Redraw canvas
        self.forecast_canvas.draw()
    def update_journal_display(self, mood, notes):
        """Update journal display with new mood and notes"""
        self.mood_var.set(mood)
        self.journal_text.delete("1.0", tk.END)
        self.journal_text.insert(tk.END, notes)
        self.journal_text.see(tk.END)   
    def clear_journal(self):
        """Clear the journal text area"""
        self.journal_text.delete("1.0", tk.END)
        self.mood_var.set("")
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == 'light':
            self.root.configure(bg='#333333')
            self.main_frame.configure(bg='#444444')
            self.current_theme = 'dark'
        else:
            self.root.configure(bg='#f0f0f0')
            self.main_frame.configure(bg='#f0f0f0')
            self.current_theme = 'light'
        
        # Update all widgets to match new theme
        for widget in self.main_frame.winfo_children():
            widget.configure(style=f"{self.current_theme}.TFrame")
        # Update labels
        for label in self.main_frame.winfo_children():
            if isinstance(label, ttk.Label):
                label.configure(style=f"{self.current_theme}.TLabel")
        # Update buttons
        for button in self.main_frame.winfo_children(): 
            if isinstance(button, ttk.Button):
                button.configure(style=f"{self.current_theme}.TButton") 
        # Update entry fields
        for entry in self.main_frame.winfo_children():
            if isinstance(entry, ttk.Entry):
                entry.configure(style=f"{self.current_theme}.TEntry")
        # Update comboboxes
        for combo in self.main_frame.winfo_children():
            if isinstance(combo, ttk.Combobox):
                combo.configure(style=f"{self.current_theme}.TCombobox")
        # Update text areas
        for text in self.main_frame.winfo_children():
            if isinstance(text, tk.Text):
                text.configure(bg='#ffffff' if self.current_theme == 'light' else '#555555',
                               fg='#000000' if self.current_theme == 'light' else '#ffffff',
                               insertbackground='black' if self.current_theme == 'light' else 'white')
        # Update background image if available
        if self.bg_label and self.bg_image: 
            self.bg_label.configure(image=self.bg_image)
            self.bg_label.image = self.bg_image
        # Update forecast canvas
        if self.forecast_canvas:
            self.forecast_canvas.get_tk_widget().configure(bg='#ffffff' if self.current_theme == 'light' else '#555555')
            self.forecast_canvas.draw()
        # Update weather icon
        if self.weather_icon:
            self.weather_icon.configure(bg='#ffffff' if self.current_theme == 'light' else '#555555')
            if self.weather_icon.image:
                self.weather_icon.image = self.weather_icon.image
            self.weather_icon.configure(foreground='#000000' if self.current_theme == 'light' else '#ffffff')
