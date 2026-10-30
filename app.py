import os
import json
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Root directory for serving frontend files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
I18N_DIR = os.path.join(BASE_DIR, 'assets', 'i18n')

# ── Sample In-Memory Database ────────────────────────────────────────────────
DEFAULT_MEDICATIONS = [
    {
        "id": 1,
        "name": "Donepezil (5mg)",
        "time": "Morning (08:00 AM)",
        "purpose": "Memory & Cognitive Care",
        "taken": True,
        "icon": "💊"
    },
    {
        "id": 2,
        "name": "Amlodipine (5mg)",
        "time": "Afternoon (01:00 PM)",
        "purpose": "Blood Pressure Control",
        "taken": False,
        "icon": "🩺"
    },
    {
        "id": 3,
        "name": "Vitamin B-Complex",
        "time": "Evening (07:30 PM)",
        "purpose": "Nerve & General Health",
        "taken": False,
        "icon": "🌿"
    }
]

DEFAULT_VITALS = {
    "patient_name": "Bimal Hazarika",
    "age": 73,
    "condition": "Mild Cognitive Impairment (Dementia Stage 2)",
    "heart_rate": 74,
    "blood_pressure": "120/80 mmHg",
    "safe_zone": "Safe at Home (Guwahati, Assam)",
    "safe_zone_status": "inside",
    "coordinates": {"lat": 26.1445, "lng": 91.7362},
    "battery_level": 88
}

DEFAULT_FAMILY = [
    {
        "id": 1,
        "name": "Sunita Hazarika",
        "relation": "Wife (48 Years Together)",
        "avatar": "👵",
        "color": "#E9D5FF",
        "speech": "This is Sunita, your beloved wife of 48 years. You are safe together at home."
    },
    {
        "id": 2,
        "name": "Rohit Hazarika",
        "relation": "Son (Working in Guwahati)",
        "avatar": "👨‍💼",
        "color": "#BFDBFE",
        "speech": "This is your son Rohit. He loves you very much and calls every afternoon."
    },
    {
        "id": 3,
        "name": "Ananya Barua",
        "relation": "Daughter (Family Caregiver)",
        "avatar": "👩‍⚕️",
        "color": "#FEF08A",
        "speech": "This is your daughter Ananya. She prepared your evening tea and medicines."
    },
    {
        "id": 4,
        "name": "Meera",
        "relation": "Granddaughter (Age 8)",
        "avatar": "👧",
        "color": "#FED7AA",
        "speech": "This is your sweet granddaughter Meera. She is drawing pictures for you."
    }
]

LANGUAGES = [
    {"code": "en", "name": "English", "native": "English", "flag": "🇬🇧", "greeting": "Good day! Welcome to Remember It."},
    {"code": "hi", "name": "Hindi", "native": "हिन्दी", "flag": "🇮🇳", "greeting": "नमस्ते! रिमेम्बर इट में आपका स्वागत है।"},
    {"code": "as", "name": "Assamese", "native": "অসমীয়া", "flag": "🦏", "greeting": "নমস্কাৰ! আপোনাক স্বাগতম জনাইছো।"},
    {"code": "mni", "name": "Manipuri", "native": "মৈতৈলোন্", "flag": "🦌", "greeting": "খুরুমজরি! অদোমবু তরাম্না ওকচরি।"},
    {"code": "kha", "name": "Khasi", "native": "Khasi", "flag": "🌧️", "greeting": "Khublei shibun! Wan bah sha Remember It."},
    {"code": "lus", "name": "Mizo", "native": "Mizo ṭawng", "flag": "🌸", "greeting": "Chibai! Dam takin lo awm rawh le."},
    {"code": "bod", "name": "Bodo", "native": "बड़ो", "flag": "🌾", "greeting": "गोजोनथों! नोंथांखौ बरायबाय।"},
    {"code": "garo", "name": "Garo", "native": "A·chik", "flag": "🏔️", "greeting": "Salam! Remember It-ona rimchaksoa."}
]

# State store
medications_data = list(DEFAULT_MEDICATIONS)
cognitive_scores = [
    {"day": "Mon", "score": 75},
    {"day": "Tue", "score": 82},
    {"day": "Wed", "score": 88},
    {"day": "Thu", "score": 78},
    {"day": "Fri", "score": 90},
    {"day": "Sat", "score": 85},
    {"day": "Sun", "score": 92}
]

# ── API Routes ───────────────────────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        "status": "healthy",
        "app": "NER Dementia Care - Remember It",
        "runtime": "Python / Flask",
        "version": "2.1.0"
    })

@app.route('/api/languages', methods=['GET'])
def get_languages():
    return jsonify(LANGUAGES)

@app.route('/api/translations/<lang_code>', methods=['GET'])
def get_translation(lang_code):
    filename = f"{lang_code}.json"
    filepath = os.path.join(I18N_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Language translation not found"}), 404

@app.route('/api/medications', methods=['GET'])
def get_medications():
    return jsonify(medications_data)

@app.route('/api/medications', methods=['POST'])
def add_medication():
    body = request.get_json() or {}
    name = body.get('name', '').strip()
    time = body.get('time', '').strip()
    purpose = body.get('purpose', 'Prescribed Care').strip()
    if not name:
        return jsonify({"error": "Medication name is required"}), 400

    new_med = {
        "id": len(medications_data) + 1,
        "name": name,
        "time": time or "Daily",
        "purpose": purpose,
        "taken": False,
        "icon": "💊"
    }
    medications_data.append(new_med)
    return jsonify({"success": True, "medication": new_med}), 201

@app.route('/api/medications/<int:med_id>/toggle', methods=['POST', 'PUT'])
def toggle_medication(med_id):
    for med in medications_data:
        if med['id'] == med_id:
            med['taken'] = not med['taken']
            return jsonify({"success": True, "medication": med})
    return jsonify({"error": "Medication not found"}), 404

@app.route('/api/vitals', methods=['GET'])
def get_vitals():
    return jsonify(DEFAULT_VITALS)

@app.route('/api/family', methods=['GET'])
def get_family():
    return jsonify(DEFAULT_FAMILY)

@app.route('/api/scores', methods=['GET'])
def get_scores():
    return jsonify(cognitive_scores)

@app.route('/api/scores', methods=['POST'])
def save_score():
    body = request.get_json() or {}
    score = body.get('score', 90)
    day = body.get('day', 'Today')
    moves = body.get('moves', 0)
    cognitive_scores.append({"day": day, "score": min(score, 100), "moves": moves})
    return jsonify({"success": True, "history": cognitive_scores[-7:]})

@app.route('/api/sos', methods=['POST'])
def log_sos():
    body = request.get_json() or {}
    return jsonify({
        "status": "SOS_DISPATCHED",
        "patient": DEFAULT_VITALS['patient_name'],
        "location": DEFAULT_VITALS['safe_zone'],
        "coordinates": DEFAULT_VITALS['coordinates'],
        "contacts_alerted": [
            {"role": "Ambulance", "phone": "108"},
            {"role": "Emergency Helpline", "phone": "112"},
            {"role": "Dr. Sharma (Neurology)", "phone": "+91-94350-12345"},
            {"role": "Family (Rohit)", "phone": "+91-98640-54321"}
        ]
    })

# ── Static & Frontend Serving ────────────────────────────────────────────────

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if os.path.exists(os.path.join(BASE_DIR, filename)):
        return send_from_directory(BASE_DIR, filename)
    return send_from_directory(BASE_DIR, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌱 NER Dementia Care Python Server running at http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
