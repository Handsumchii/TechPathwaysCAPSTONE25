# Week 11 Reflection – Capstone Project Setup

---

## Fellow Details

| Field               | Your Entry                        |
|--------------------|-----------------------------------|
| Name               | Devin Cambridge                   |
| GitHub Username    | Dcambridge7188                    |
| Preferred Feature Track | Interactive                    |
| Team Interest      | Yes — Project Owner               |

---

## Week 11 Reflection

**Key Takeaways:**
- The capstone project is designed to reflect personal growth and real-world application.
- Clear milestones are set across Weeks 12–17 to guide feature development.
- We are expected to use tools like GitHub, APIs, and Tkinter in a practical way.
- Office hours and Slack are recommended support channels.
- Final submission includes a functional app and a demonstration.

**Concept Connections:**
- Strongest: API integration, Tkinter GUI design, SQLite3 database handling.
- Need more practice: Error handling, unit testing, packaging for deployment.

**Early Challenges:**
- Securing and loading the OpenWeatherMap API key safely.
- Setting up a clean project folder structure.
- Deciding on scalable features that reflect both creativity and feasibility.

**Support Strategies:**
- Attend Friday afternoon office hours for UI-related feedback.
- Ask questions in Slack #capstone-support for edge case handling.
- Use GitHub issues and milestones for project tracking.

---

## Feature Selection Rationale

| #  | Feature Name             | Difficulty (1–3) | Why You Chose It / Learning Goal                     |
|----|--------------------------|------------------|------------------------------------------------------|
| 1  | Weather Mood Journal     | 2                | Combine weather and daily mood to explore correlation. |
| 2  | Animated Weather Icons   | 3                | Practice canvas/dynamic UI using conditions.         |
| 3  | Forecast Comparison Tool | 2                | Learn to work with multiple datasets/APIs.           |
| –  | Enhancement: Dark Mode   | –                | Improve UI/UX and practice theme switching in Tkinter.|

---

## High-Level Architecture Sketch

**Folder Structure:**
/project-root
|-- main.py
|-- config.py
|-- .env
|-- /data
|-- /features
|-- weather_journal.py
|-- animated_icons.py
|-- forecast_comparison.py
|-- /docs
|-- Week11_Reflection.md
|-- README.md


---

## Data Model Plan

| File/Table Name         | Format  | Example Row                                 |
|-------------------------|---------|---------------------------------------------|
| weather_history.txt     | txt     | 2025-06-09,New York,82°F,Cloudy             |
| journal_entries.csv     | csv     | 2025-06-09,Happy,Good day at work           |
| forecast_data.json      | json    | {"date": "2025-06-10", "high": 85, "low": 68}|

---

## Personal Project Timeline (Weeks 12–17)

| Week | Monday        | Tuesday        | Wednesday      | Thursday       | Key Milestone         |
|------|---------------|----------------|----------------|----------------|------------------------|
| 12   | API setup     | Error handling | Tkinter shell  | Buffer day     | Basic working app      |
| 13   | Feature 1     |                |                | Integrate      | Feature 1 complete     |
| 14   | Feature 2     |                | Review & test  | Finish         | Feature 2 complete     |
| 15   | Feature 3     | Polish UI      | Error passing  | Refactor       | All features complete  |
| 16   | Enhancement   | Docs           | Tests          | Packaging      | Ready-to-ship app      |
| 17   | Rehearse      | Buffer         | Showcase       | –              | Demo Day               |

---

## Risk Assessment

| Risk               | Likelihood | Impact | Mitigation Plan                                |
|--------------------|------------|--------|-------------------------------------------------|
| API Rate Limit     | Medium     | Medium | Add caching or retry logic w/ exponential backoff |
| Feature Overload   | High       | High   | Prioritize core functionality and scale back    |
| UI Bugs in Tkinter | Medium     | Medium | Regular testing and UI feedback from peers      |

---

## Support Requests

- Help structuring canvas animations in Tkinter
- Guidance on safely caching or storing API results
- Clarification on using `.env` in Codespaces/GitHub

---

## Before Monday (Start of Week 12)

- [x] `main.py`, `config.py`, and `/data/` folder pushed to repo
- [x] `.env` created locally with OpenWeatherMap API key
- [x] `/features/` includes stub files like `weather_journal.py`
- [x] `README.md` first draft committed and pushed
- [x] Booked office hours for UI/animation questions

---

## 🔗 Final Submission Checklist

- [x] `Week11_Reflection.md` completed
- [x] File uploaded to GitHub repo `/docs/`
- [ ] Repo link submitted to Canvas ✅

