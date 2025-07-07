import csv
from datetime import datetime
import os

DATA_FILE = os.path.join("data", "journal_entries.csv")

def add_journal_entry(date, location, mood, notes, weather_summary):
    """
    Appends a journal entry to the journal_entries.csv file.
    """
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, location, mood, notes, weather_summary])

def load_journal_entries():
    """
    Returns a list of all saved journal entries.
    """
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, mode="r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        return list(reader)