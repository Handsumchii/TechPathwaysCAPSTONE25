# TechPathwaysCAPSTONE25
# Interactive Weather App – Capstone Project

## Overview

This project is an interactive, Tkinter-based desktop application that displays real-time weather data, a personal weather journal, and animated visual feedback based on current conditions. It was developed as part of the Justice Through Code Capstone experience to demonstrate applied Python development, API integration, and UI design.

---

## Features

| Feature                 | Description |
|------------------------|-------------|
| **Real-Time Weather Display** | Pulls current weather data from the OpenWeatherMap API for any valid location. |
| **Weather Mood Journal** | Lets users record a mood or note alongside daily weather conditions. |
| **Animated Weather Icons** | Visual feedback like sun, rain, and clouds reflect current weather dynamically. |
| **Dark Mode Support** | Toggle between light and dark themes to enhance user experience. |
| **Forecast Comparison Tool** | Shows side-by-side temperature forecasts across multiple cities. |

---

## Project Structure

/interactive-weather-app
│
├── main.py # Entry point for the application
├── config.py # Configuration loader (API key, settings)
├── .env # Stores API key (NOT committed)
├── /data/ # Local storage for journal and history
│ └── weather_history.txt
├── /features/
│ ├── weather_journal.py # Journal feature
│ ├── animated_icons.py # Icon/animation logic
│ └── forecast_comparison.py # Forecast tool
├── /docs/
│ └── Week11_Reflection.md # Project setup and planning document
└── README.md


## How To Use It

### 1. Clone the project

```bash
git clone https://github.com/YOUR_USERNAME/interactive-weather-app.git
cd interactive-weather-app
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Set up your .env file
Create a .env file and add your API key:

env
Copy
Edit
OPENWEATHER_API_KEY=your_api_key_here
4. Run the app
bash
Copy
Edit
python main.py
 Tools I Used
Python

Tkinter for building the GUI

OpenWeatherMap API

Matplotlib for visuals

Pandas for working with CSV/text data

dotenv for handling the API key safely

 Development Timeline
Week	Focus
12	Basic UI and API setup
13	Weather Journal feature
14	Forecast comparison
15	Animated weather icons
16	Dark mode + polish
17	Testing + showcase

 Lessons & Growth
This project pushed me to think about user experience, code structure, and handling real-time data. I had to overcome some blockers (API limits, error handling, animation quirks), but I leaned into Slack support and office hours to move forward. The biggest win? Seeing the features actually work together and feel cohesive.

 About Me
Devin Cambridge
GitHub:https://github.com/Handsumchii
Email: Dcambridge7188@gmail.com
I’m focused on tech that brings people together, builds awareness, and creates new opportunities—especially for justice-impacted communities. This app is one small step in that direction.
