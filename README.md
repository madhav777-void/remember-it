# 🌱 Remember It – NER Dementia Care
> **Culturally-Inclusive Multilingual Dementia & Elderly Care Companion for North East India**  
> Powered by **Python (Flask)** Serverless Architecture & High-Performance Web Frontend.

[![Vercel Deployment Ready](https://img.shields.io/badge/Vercel-Deployment%20Ready-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Python 3.x](https://img.shields.io/badge/Python-3.x%20Flask-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Languages](https://img.shields.io/badge/Languages-8%20NER%20Dialects-2E7D6E?style=for-the-badge)](#-multilingual-support)
[![Accessibility](https://img.shields.io/badge/WCAG-AA%20Compliant-E87C3E?style=for-the-badge)](#-elderly-friendly-accessibility)

---

## 🌟 Overview

**Remember It** is an accessible, dementia-centric companion app built specifically for the elderly citizens of North East India and their family caregivers. It addresses the emotional, clinical, and linguistic barriers of dementia care by combining:

- **Ultra-Simple, Calming UI**: High contrast, tactile buttons, distraction-free cards designed specifically for dementia patients.
- **8 North East Regional Languages**: Assamese, Manipuri (Meitei), Khasi, Mizo, Bodo, Garo, Hindi, and English with native voice greetings.
- **3D Physics Brain Games**: Memory matching game featuring regional cultural heritage (One-Horned Rhino, Assam Tea, Sangai Deer, Living Root Bridge, Anthurium Flower, Bihu Dhol) with card-flip physics and positive reinforcement audio fanfare.
- **Daily Medication Reminders**: Easy 1-tap checklists for Morning, Afternoon, and Evening doses.
- **Family Reminiscence Photo Album**: Tap to hear comforting voice notes from family members (Wife, Son, Daughter, Granddaughter).
- **Persistent Emergency SOS**: Instant emergency siren and 1-tap speed dials for Ambulance (108), Police (112), GMCH Doctors, and Family.
- **Caregiver Health Dashboard**: Patient safe-zone geofence indicator, heart rate vitals, medication adherence tracking, and 7-day cognitive score trend chart.

---

## 🚀 1-Click Vercel Deployment

This project is configured with `vercel.json` and Python Serverless functions (`api/index.py`), ready for instant zero-config deployment on Vercel.

### Steps to Deploy:
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Switch to Python backend and simplified accessible UI"
   git push origin main
   ```
2. **Deploy on Vercel**:
   - Go to [vercel.com](https://vercel.com) and sign in.
   - Click **"Add New..."** ➔ **"Project"**.
   - Select your GitHub repository (`remember-it`).
   - Click **"Deploy"**.
   - Vercel automatically detects the Python runtime (`@vercel/python`) and static assets!

---

## 💻 Local Development (Python)

To run the full-stack Python application locally:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the Python Flask server
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🛠️ Tech Stack & Architecture

| Component | Technology |
|---|---|
| **Backend & API** | Python 3.x, Flask (`app.py`, `api/index.py`) |
| **Serverless Deployment** | Vercel (`vercel.json`, `@vercel/python`) |
| **Frontend** | Semantic HTML5, Modular CSS3 (Design Tokens), Vanilla JavaScript (ES6+) |
| **Physics & Animations** | CSS 3D Transforms (`perspective`, `rotateY`, cubic-bezier physics) |
| **Audio Engine** | Web Audio API (Synthesized chimes, clicks, fanfare, siren) |
| **Voice & Speech** | Web Speech API (`SpeechSynthesis`) |
| **Localization** | 8 JSON Translation dictionaries (`assets/i18n/`) |

---

## 📡 API Endpoints

- `GET /api/health` — Service health and version check.
- `GET /api/languages` — List of 8 supported regional languages and greetings.
- `GET /api/translations/<lang>` — Translation dictionary for the requested dialect.
- `GET /api/medications` — Retrieve daily medication schedule and taken status.
- `POST /api/medications/<id>/toggle` — Toggle medication taken/pending status.
- `POST /api/medications` — Add a new prescription reminder.
- `GET /api/vitals` — Patient safe-zone status, heart rate, and GPS coordinates.
- `GET /api/scores` — 7-Day cognitive memory game test history.
- `POST /api/scores` — Record a completed memory game session score.
- `POST /api/sos` — Trigger emergency alert log with GPS coordinates and dispatch list.
- `GET /api/family` — Family reminiscence members and speech cues.

---

## 👥 Culture & Community

Designed with care and respect for the diverse cultures and communities across the Eight Sister States of North East India.
