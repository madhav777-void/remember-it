import os
import json
import functools
from flask import (
    Flask, jsonify, request, render_template,
    redirect, url_for, session, flash, send_from_directory
)

# Root directory configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
I18N_DIR = os.path.join(BASE_DIR, 'assets', 'i18n')

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)

# Secret key for secure session handling
app.secret_key = os.environ.get('SECRET_KEY', 'remember-it-dementia-care-2026-secret-key-ner')

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
    "safe_zone": "Inside Safe Zone (Home - Guwahati, Assam)",
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
        "speech": "This is Sunita, your beloved wife of 48 years. You are safe together at home in Guwahati."
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
        "speech": "This is your daughter Ananya. She prepared your warm evening tea and fresh medicines."
    },
    {
        "id": 4,
        "name": "Meera",
        "relation": "Granddaughter (Age 8)",
        "avatar": "👧",
        "color": "#FED7AA",
        "speech": "This is your sweet granddaughter Meera. She is drawing beautiful pictures for you."
    }
]

LANGUAGES = [
    {"code": "en", "name": "English", "native": "English", "flag": "🇬🇧", "greeting": "Good day! Welcome to Remember It."},
    {"code": "as", "name": "Assamese", "native": "অসমীয়া", "flag": "🦏", "greeting": "নমস্কাৰ! আপোনাক স্বাগতম জনাইছো।"},
    {"code": "hi", "name": "Hindi", "native": "हिन्दी", "flag": "🇮🇳", "greeting": "नमस्ते! रिमेम्बर इट में आपका स्वागत है।"},
    {"code": "mni", "name": "Manipuri", "native": "মৈতৈলোন্", "flag": "🦌", "greeting": "খুরুমজরি! অদোমবু তরাম্না ওকচরি।"},
    {"code": "kha", "name": "Khasi", "native": "Khasi", "flag": "🌧️", "greeting": "Khublei shibun! Wan bah sha Remember It."},
    {"code": "lus", "name": "Mizo", "native": "Mizo ṭawng", "flag": "🌸", "greeting": "Chibai! Dam takin lo awm rawh le."},
    {"code": "bod", "name": "Bodo", "native": "बड़ो", "flag": "🌾", "greeting": "गोजोनथों! नोंथांखौ बरायबाय।"},
    {"code": "garo", "name": "Garo", "native": "A·chik", "flag": "🏔️", "greeting": "Salam! Remember It-ona rimchaksoa."}
]

# ── SPECIAL FEATURE: Individual Dementia Life Story Profile ─────────────────
DEFAULT_LIFE_STORY = {
    "childhood": "Born and raised along the banks of the Brahmaputra River in Tezpur, Assam. Grew up in a joint family with four siblings.",
    "occupation": "Senior Forestry Officer with Assam Forest Department (34 years of service). Worked extensively in Kaziranga National Park protecting rhinos and wildlife.",
    "hobbies": ["Gardening indigenous orchid species", "Playing the Bihu Dhol and Flute", "Fishing in river streams", "Listening to Bhupen Hazarika folk songs"],
    "music": ["Bhupen Hazarika Classics (Manuhe Manuhor Babe)", "Zubeen Garg Folk Melodies", "Borgeet devotional prayers", "Rabindra Sangeet"],
    "life_events": [
        {"year": 1953, "title": "Born in Tezpur, Assam"},
        {"year": 1978, "title": "Married Sunita in Guwahati - 48 years of love and companionship"},
        {"year": 1982, "title": "Joined Assam Forest Service at Kaziranga"},
        {"year": 1985, "title": "Birth of son Rohit; daughter Ananya born in 1989"},
        {"year": 2016, "title": "Retired as Divisional Forest Officer with state honors"}
    ],
    "favorite_foods": ["Traditional Assam Khar & Masor Tenga (sour fish curry)", "Fresh green tea with tulsi leaves", "Pitha sweets during Bihu", "Warm rice with mashed potatoes (Alu Pitika)"],
    "comfort_triggers": [
        "Playing soft bamboo flute or Bhupen Hazarika songs",
        "Gentle hand massage with lavender or mustard oil",
        "Holding family photo album of Kaziranga trips",
        "Sitting on the garden verandah in morning sunlight with warm tea",
        "Speaking in native Assamese with family"
    ],
    "distress_triggers": [
        "Loud sudden noises, slamming doors or sirens",
        "Rushing or multiple staff speaking at once",
        "Dark corridors or unlit rooms after sunset (sundowning)",
        "Feeling confined or unable to see an open window"
    ],
    "safety_preferences": "Always explain care steps slowly in Assamese before starting. Keep his spectacles and family photo frame within reach on the bedside table."
}

# ── 22 Clinical Modules State Store ──────────────────────────────────────────
CLINICAL_MODULES_STATE = {
    "food_fluid_logs": [
        {"time": "08:30 AM", "meal": "Breakfast", "item": "Warm rice gruel, boiled egg, fresh papaya", "consumed": "85%", "fluid_ml": 250, "swallowing": "Normal", "logged_by": "Nurse Sunita"},
        {"time": "01:15 PM", "meal": "Lunch", "item": "Masor Tenga fish stew, soft steamed rice, dal", "consumed": "90%", "fluid_ml": 300, "swallowing": "Normal", "logged_by": "Nurse Sunita"},
        {"time": "05:00 PM", "meal": "Afternoon Tea", "item": "Assam green tea with soft Marie biscuit", "consumed": "100%", "fluid_ml": 200, "swallowing": "Normal", "logged_by": "Caregiver Rohit"}
    ],
    "news2_observations": [
        {"time": "08:00 AM", "bp": "120/80", "pulse": 74, "temp": "36.8°C", "resp": 16, "spo2": "98%", "glucose": "108 mg/dL", "pain": "0/10", "news2_score": 0, "status": "Low Risk / Normal"},
        {"time": "02:00 PM", "bp": "122/82", "pulse": 76, "temp": "36.9°C", "resp": 17, "spo2": "98%", "glucose": "124 mg/dL", "pain": "1/10", "news2_score": 0, "status": "Low Risk / Normal"}
    ],
    "behaviour_logs": [
        {"time": "11:00 AM", "mood": "Happy & Engaged", "behaviour": "Enjoyed flower arranging activity in sensory garden", "trigger": "None", "intervention": "Offered positive encouragement", "outcome": "Calm and smiling"},
        {"time": "06:15 PM", "mood": "Mild Sundowning Restlessness", "behaviour": "Pacing near room door asking about his forest office", "trigger": "Twilight dimming lights", "intervention": "Turned on warm lights, offered warm tea, played Bhupen Hazarika music", "outcome": "Settled down peacefully within 15 minutes"}
    ],
    "activity_logs": [
        {"activity": "Cultural Memory Match Game", "category": "Cognitive Stimulation", "duration": "20 mins", "participation": "Prompted", "mood_before": "Quiet", "mood_after": "Delighted", "benefit": "Recalled Kaziranga rhino memories"},
        {"activity": "Sensory Orchid Garden Walk", "category": "Creative & Outdoor", "duration": "25 mins", "participation": "Independent with supervision", "mood_before": "Neutral", "mood_after": "Very Happy", "benefit": "Physical movement and fresh air"}
    ],
    "shift_handovers": [
        {"shift": "Morning Shift (07:00 - 15:00)", "staff": "Nurse Pranjal & Care Assistant Bhaswati", "vitals_summary": "Stable NEWS2=0", "meds_summary": "Morning Donepezil taken, Amlodipine taken", "diet_summary": "Fluid target 750ml met", "incidents": "Zero falls, zero safeguarding concerns", "next_shift_actions": "Ensure 07:30 PM Vitamin B-Complex given; watch for sunset restlessness around 18:00"}
    ]
}

# ── In-Memory User Store (Pre-seeded Demo Accounts) ──────────────────────────
USERS = {
    "9876543210": {
        "phone": "9876543210",
        "name": "Bimal Hazarika",
        "role": "patient",
        "password": "demo123",
        "age": 73,
        "condition": "Mild Cognitive Impairment (Dementia Stage 2)",
        "location": "Guwahati, Assam",
        "safe_zone": "Inside Safe Zone (Home)",
        "linked_caregiver_phone": "1234567890",
        "last_mood": {"emoji": "😊", "label": "Happy & Calm"}
    },
    "1234567890": {
        "phone": "1234567890",
        "name": "Rohit Hazarika",
        "role": "caregiver",
        "password": "demo123",
        "relation": "Son (Primary Caregiver)",
        "linked_patient_phone": "9876543210"
    }
}

# Dynamic application state
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

# ── Authentication Helpers & Decorators ─────────────────────────────────────

def get_current_user():
    """Retrieve current logged in user from session and user store."""
    phone = session.get('user_phone')
    if phone and phone in USERS:
        return USERS[phone]
    return None

def login_required(view_func):
    """Decorator ensuring that a route can only be accessed by authenticated users."""
    @functools.wraps(view_func)
    def decorated_function(*args, **kwargs):
        phone = session.get('user_phone')
        if not phone or phone not in USERS:
            flash('Please sign in to access this page.', 'warning')
            return redirect(url_for('auth_page'))
        return view_func(*args, **kwargs)
    return decorated_function

# ── Multi-Page Application Routing ──────────────────────────────────────────

@app.route('/')
def index_route():
    """Root route: redirects to patient home, caregiver dashboard, or auth page."""
    user = get_current_user()
    if user:
        if user.get('role') == 'caregiver':
            return redirect(url_for('caregiver_dashboard'))
        return redirect(url_for('patient_home'))
    return redirect(url_for('auth_page'))

@app.route('/auth', methods=['GET'])
def auth_page():
    """Auth view: split login & register for both Patient and Caregiver."""
    user = get_current_user()
    if user:
        if user.get('role') == 'caregiver':
            return redirect(url_for('caregiver_dashboard'))
        return redirect(url_for('patient_home'))
    return render_template('auth.html')

@app.route('/auth/login', methods=['POST'])
def auth_login():
    """Authenticate user with phone and password."""
    phone = request.form.get('phone', '').strip()
    password = request.form.get('password', '').strip()

    if not phone or not password:
        flash('Please enter both your phone number and password.', 'error')
        return redirect(url_for('auth_page', tab='login'))

    user = USERS.get(phone)
    if user and user.get('password') == password:
        # Establish authenticated session
        session['user_phone'] = phone
        session['user_role'] = user.get('role', 'patient')
        session['user_name'] = user.get('name', 'User')
        session.permanent = True

        flash(f"Welcome back, {user.get('name')}!", 'success')
        if user.get('role') == 'caregiver':
            return redirect(url_for('caregiver_dashboard'))
        return redirect(url_for('patient_home'))

    flash('Invalid phone number or password. You can use the instant demo buttons below!', 'error')
    return redirect(url_for('auth_page', tab='login'))

@app.route('/auth/register', methods=['POST'])
def auth_register():
    """Register a new Patient or Caregiver account."""
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    role = request.form.get('role', 'patient').strip()
    password = request.form.get('password', '').strip()
    age = request.form.get('age', '').strip()
    relation = request.form.get('relation', '').strip()
    linked_patient_phone = request.form.get('linked_patient_phone', '').strip()

    if not name or not phone or not password:
        flash('Name, phone number, and password are required.', 'error')
        return redirect(url_for('auth_page', tab='register'))

    if phone in USERS:
        flash('An account with this phone number already exists. Please sign in.', 'error')
        return redirect(url_for('auth_page', tab='login'))

    # Build new user object
    new_user = {
        "phone": phone,
        "name": name,
        "role": role,
        "password": password
    }

    if role == 'patient':
        new_user['age'] = int(age) if age.isdigit() else 70
        new_user['condition'] = "Mild Cognitive Impairment (Dementia Care)"
        new_user['location'] = "Guwahati, Assam"
        new_user['safe_zone'] = "Inside Safe Zone (Home)"
        new_user['last_mood'] = {"emoji": "😊", "label": "Happy & Calm"}
        new_user['linked_caregiver_phone'] = ""
    else:
        new_user['relation'] = relation or "Family Caregiver"
        new_user['linked_patient_phone'] = linked_patient_phone or "9876543210"

    USERS[phone] = new_user

    # Log user in
    session['user_phone'] = phone
    session['user_role'] = role
    session['user_name'] = name
    session.permanent = True

    flash(f"Account successfully created! Welcome, {name}.", 'success')
    if role == 'caregiver':
        return redirect(url_for('caregiver_dashboard'))
    return redirect(url_for('patient_home'))

@app.route('/auth/logout', methods=['GET'])
def auth_logout():
    """Log out current user and clear session."""
    session.clear()
    flash('You have been safely signed out. Have a peaceful day!', 'info')
    return redirect(url_for('auth_page'))

# ── Patient Pages ────────────────────────────────────────────────────────────

@app.route('/patient', methods=['GET'])
@login_required
def patient_home():
    """Patient Home: personalized greeting, real-time clock, quick cards, daily mood check."""
    user = get_current_user()
    return render_template(
        'patient_home.html',
        user=user,
        medications=medications_data,
        languages=LANGUAGES
    )

@app.route('/patient/medicines', methods=['GET'])
@login_required
def patient_medicines():
    """Dedicated Daily Medicine Checklist page."""
    user = get_current_user()
    return render_template(
        'patient_medicines.html',
        user=user,
        medications=medications_data
    )

@app.route('/patient/game', methods=['GET'])
@app.route('/patient/games', methods=['GET'])
@login_required
def patient_game():
    """Dedicated Cognitive Brain Games Hub page."""
    user = get_current_user()
    return render_template(
        'patient_game.html',
        user=user
    )

@app.route('/patient/drawing', methods=['GET'])
@app.route('/patient/art', methods=['GET'])
@login_required
def patient_drawing():
    return redirect(url_for('patient_game') + '?tab=drawing')

@app.route('/patient/family', methods=['GET'])
@login_required
def patient_family():
    """Dedicated Loved Ones Reminiscence Album page."""
    user = get_current_user()
    return render_template(
        'patient_family.html',
        user=user,
        family_members=DEFAULT_FAMILY
    )

# ── Caregiver Pages ──────────────────────────────────────────────────────────

@app.route('/caregiver', methods=['GET'])
@login_required
def caregiver_dashboard():
    """Caregiver Dashboard: connected patient vitals, adherence tracker, 7-day cognitive chart."""
    user = get_current_user()
    
    # Locate linked patient
    linked_phone = user.get('linked_patient_phone', '9876543210')
    patient = USERS.get(linked_phone)
    if not patient:
        patient = {
            "name": DEFAULT_VITALS["patient_name"],
            "age": DEFAULT_VITALS["age"],
            "condition": DEFAULT_VITALS["condition"],
            "safe_zone": DEFAULT_VITALS["safe_zone"],
            "last_mood": {"emoji": "😊", "label": "Happy & Calm"}
        }

    return render_template(
        'caregiver_dashboard.html',
        user=user,
        patient=patient,
        medications=medications_data,
        vitals=DEFAULT_VITALS,
        scores=cognitive_scores
    )

@app.route('/caregiver/emergency', methods=['GET'])
@login_required
def caregiver_emergency():
    """Caregiver Emergency Helpline & Protocol Directory."""
    user = get_current_user()
    linked_phone = user.get('linked_patient_phone', '9876543210')
    patient = USERS.get(linked_phone) or {"name": DEFAULT_VITALS["patient_name"]}
    return render_template(
        'caregiver_emergency.html',
        user=user,
        patient=patient
    )

@app.route('/caregiver/care-management', methods=['GET'])
@login_required
def caregiver_care_management():
    """Comprehensive 22-Module Dementia Patient Care Management System."""
    user = get_current_user()
    linked_phone = user.get('linked_patient_phone', '9876543210')
    patient = USERS.get(linked_phone) or {
        "name": DEFAULT_VITALS["patient_name"],
        "age": DEFAULT_VITALS["age"],
        "condition": DEFAULT_VITALS["condition"],
        "safe_zone": DEFAULT_VITALS["safe_zone"]
    }
    return render_template(
        'caregiver_care_management.html',
        user=user,
        patient=patient,
        medications=medications_data,
        life_story=DEFAULT_LIFE_STORY,
        clinical_state=CLINICAL_MODULES_STATE
    )

@app.route('/patient/lifestory', methods=['GET'])
@app.route('/caregiver/lifestory', methods=['GET'])
@login_required
def patient_lifestory():
    """Individual Dementia Life Story Profile Book."""
    user = get_current_user()
    return render_template(
        'patient_lifestory.html',
        user=user,
        life_story=DEFAULT_LIFE_STORY
    )

# ── API Routes (Preserved & Extended) ────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        "status": "healthy",
        "app": "NER Dementia Care - Remember It",
        "runtime": "Python / Flask",
        "version": "2.2.0",
        "architecture": "Multi-Page with Session Auth"
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
    body = request.get_json(silent=True) or {}
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
    body = request.get_json(silent=True) or {}
    score = body.get('score', 95)
    day = body.get('day', 'Today')
    moves = body.get('moves', 0)
    cognitive_scores.append({"day": day, "score": min(score, 100), "moves": moves})
    return jsonify({"success": True, "history": cognitive_scores[-7:]})

@app.route('/api/mood', methods=['POST', 'GET'])
def handle_mood():
    """Daily mood check endpoint."""
    user = get_current_user()
    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        mood = body.get('mood', 'Happy & Calm')
        emoji = body.get('emoji', '😊')
        mood_obj = {"emoji": emoji, "label": mood}
        if user:
            user['last_mood'] = mood_obj
        # Also ensure pre-seeded patient gets updated
        USERS['9876543210']['last_mood'] = mood_obj
        return jsonify({"success": True, "mood": mood_obj})
    
    current_mood = user.get('last_mood') if user else USERS['9876543210'].get('last_mood')
    return jsonify(current_mood or {"emoji": "😊", "label": "Happy & Calm"})

@app.route('/api/sos', methods=['POST'])
def log_sos():
    body = request.get_json(silent=True) or {}
    user = get_current_user()
    patient_name = user.get('name') if user else DEFAULT_VITALS['patient_name']
    return jsonify({
        "status": "SOS_DISPATCHED",
        "patient": patient_name,
        "location": DEFAULT_VITALS['safe_zone'],
        "coordinates": DEFAULT_VITALS['coordinates'],
        "contacts_alerted": [
            {"role": "Ambulance", "phone": "108"},
            {"role": "Emergency Helpline", "phone": "112"},
            {"role": "Dr. Sharma (Neurology)", "phone": "+91-94350-12345"},
            {"role": "Family (Rohit)", "phone": "+91-98640-54321"}
        ]
    })

# ── Static File Fallback Serving ─────────────────────────────────────────────

@app.route('/styles.css')
def serve_root_styles():
    return send_from_directory(STATIC_DIR, 'styles.css')

@app.route('/app.js')
def serve_root_js():
    return send_from_directory(BASE_DIR, 'app.js')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(BASE_DIR, 'manifest.json')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌱 Remember It Multi-Page Server running at http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
