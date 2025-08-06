# TechPathwaysCAPSTONE25
🛠️ Setup Instructions
1.	Clone the Repository
bash
git clone https://github.com/yourusername/vibecheck-weather-app.git
cd vibecheck-weather-app
2.	Create a Virtual Environment (Optional but Recommended)
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3.	Install Dependencies
bash
pip install -r requirements.txt
4.	Set Up Environment Variables
Create a .env file in the root directory and add your OpenWeatherMap API key:
ini
WEATHER_API_KEY=your_api_key_here
5.	Run the App
bash
python -m weather_app.main
________________________________________
📖 Usage Guide
1.	Launch the App
Start from the welcome screen and enter your name and city.
2.	View the Weather Dashboard
o	Displays real-time weather data (temperature, humidity, etc.)
o	Toggle between °C and °F
o	View current UV index, "feels like" temp, and air quality
3.	Track Your Mood
o	Enter your mood and optional notes for the day
o	Save journal entries linked to the weather
4.	Review Journal Entries
o	Click "View Entries" to browse past moods and weather conditions
5.	View Data Visualizations
o	Compare mood trends and weather patterns with built-in charts
________________________________________
✨ Feature Summary
•	🌡️ Real-time Weather Lookup via OpenWeatherMap API
•	💬 Mood Journaling tied to current weather data
•	📊 Visual Analytics:
o	Weather trends
o	Mood vs. weather comparison charts
•	🕶️ Theme Toggle (Light/Dark mode)
•	📚 Journal History Viewer with timestamped entries
•	🔐 .env Support for secure API key storage
•	🧠 User-Friendly Interface built with Tkinter and PIL
•	🌍 Temperature Unit Switching (Celsius / Fahrenheit)

Designed to help you check the vibe of your day – both emotionally and atmospherically.
