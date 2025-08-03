import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import os
from datetime import datetime

JOURNAL_FILE = os.path.join(os.path.dirname(__file__), "journal_entries.json")

MOOD_COLORS = {
    "Happy": "green",
    "Neutral": "gray",
    "Sad": "blue",
    "Angry": "red"
}

def generate_charts():
    if not os.path.exists(JOURNAL_FILE):
        return []

    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []

    if not data:
        return []

    # Prepare data
    dates = [datetime.fromisoformat(entry["timestamp"]) for entry in data]
    temps = [entry.get("temp", 0) for entry in data]
    moods = [entry.get("mood", "Neutral") for entry in data]

    # Chart 1: Temperature over time
    fig1, ax1 = plt.subplots()
    ax1.plot(dates, temps, marker="o", linestyle="-", color="skyblue")
    ax1.set_title("Temperature Over Time")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax1.grid(True)

    # Chart 2: Mood Frequency
    fig2, ax2 = plt.subplots()
    mood_counts = {m: moods.count(m) for m in set(moods)}
    ax2.bar(mood_counts.keys(), mood_counts.values(), color=[MOOD_COLORS.get(m, "gray") for m in mood_counts])
    ax2.set_title("Mood Frequency")
    ax2.set_xlabel("Mood")
    ax2.set_ylabel("Count")

    return [fig1, fig2]
