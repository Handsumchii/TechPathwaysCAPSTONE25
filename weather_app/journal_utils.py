import json
import os
from datetime import datetime

JOURNAL_FILE = os.path.join(os.path.dirname(__file__), "journal_entries.json")

def save_journal_entry(weather_data, mood, notes, q1, q2, q3, file_path=JOURNAL_FILE):
    entry_data = {
        "city": weather_data.get("name", "Unknown"),
        "mood": mood,
        "notes": notes,
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "temp": weather_data.get("main", {}).get("temp", "N/A"),
        "timestamp": datetime.now().isoformat()
    }

    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append(entry_data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print("📝 Journal entry saved.")

def load_journal_entries(file_path=JOURNAL_FILE):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading journal entries: {e}")
            return []
    return []






