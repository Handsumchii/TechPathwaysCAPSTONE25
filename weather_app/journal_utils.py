import json
import os
from datetime import datetime

JOURNAL_FILE = os.path.join(os.path.dirname(__file__), "journal_entries.json")

def save_journal_entry(city, mood, notes, file_path=JOURNAL_FILE):
    """
    Save a journal entry as a JSON object to the file.
    Raises an exception if saving fails.
    """
    entry_data = {
        "city": city,
        "mood": mood,
        "notes": notes,
        "timestamp": datetime.now().isoformat()
    }

    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []  # file corrupted or empty, reset data list

    data.append(entry_data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print("📝 Journal entry saved.")

def load_journal_entries(file_path=JOURNAL_FILE):
    """
    Load journal entries from the JSON file.
    Returns a list of entries or empty list if none exist.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading journal entries: {e}")
            return []
    return []
