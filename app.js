/**
 * ============================================================================
 * Remember It - "NER Dementia Care"
 * Accessible Frontend Application Engine with Python API Integration
 * Preserves 3D Physics Brain Game & Web Audio Engine
 * ============================================================================
 */

class SoundEngine {
  constructor() {
    this.ctx = null;
    this.muted = false;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playClick() {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(480, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(800, this.ctx.currentTime + 0.05);

      gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.06);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start();
      osc.stop(this.ctx.currentTime + 0.06);
    } catch (e) {
      // Audio fallback
    }
  }

  playChime() {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    try {
      const notes = [523.25, 659.25, 783.99]; // C5, E5, G5
      notes.forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + i * 0.09);

        gain.gain.setValueAtTime(0.18, this.ctx.currentTime + i * 0.09);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + i * 0.09 + 0.35);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(this.ctx.currentTime + i * 0.09);
        osc.stop(this.ctx.currentTime + i * 0.09 + 0.35);
      });
    } catch (e) {}
  }

  playFanfare() {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    try {
      const fanfareNotes = [523.25, 659.25, 783.99, 1046.5];
      fanfareNotes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + idx * 0.12);

        gain.gain.setValueAtTime(0.25, this.ctx.currentTime + idx * 0.12);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + idx * 0.12 + 0.55);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(this.ctx.currentTime + idx * 0.12);
        osc.stop(this.ctx.currentTime + idx * 0.12 + 0.55);
      });
    } catch (e) {}
  }

  playSiren() {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';

      const now = this.ctx.currentTime;
      osc.frequency.setValueAtTime(700, now);
      osc.frequency.linearRampToValueAtTime(950, now + 0.3);
      osc.frequency.linearRampToValueAtTime(700, now + 0.6);
      osc.frequency.linearRampToValueAtTime(950, now + 0.9);
      osc.frequency.linearRampToValueAtTime(700, now + 1.2);

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 1.3);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 1.3);
    } catch (e) {}
  }
}

class DementiaCareApp {
  constructor() {
    this.sound = new SoundEngine();
    this.currentLang = localStorage.getItem('ner_lang') || 'en';
    this.currentMode = 'patient';

    this.languages = [
      { code: 'en', name: 'English', native: 'English', flag: '🇬🇧', greeting: 'Good day! Welcome to Remember It. You are safe and loved.' },
      { code: 'hi', name: 'Hindi', native: 'हिन्दी', flag: '🇮🇳', greeting: 'नमस्ते! रिमेम्बर इट में आपका स्वागत है। आप सुरक्षित और प्रिय हैं।' },
      { code: 'as', name: 'Assamese', native: 'অসমীয়া', flag: '🦏', greeting: 'নমস্কাৰ! আপোনাক স্বাগতম জনাইছো। আপুনি সম্পূৰ্ণ সুৰক্ষিত।' },
      { code: 'mni', name: 'Manipuri', native: 'মৈতৈলোন্', flag: '🦌', greeting: 'খুরুমজরি! অদোমবু তরাম্না ওকচরি। অদোম য়াম্না চাউনা চেকশিন্না লৈরি।' },
      { code: 'kha', name: 'Khasi', native: 'Khasi', flag: '🌧️', greeting: 'Khublei shibun! Wan bah sha Remember It. Phi long suk bad dap da ka jingieit.' },
      { code: 'lus', name: 'Mizo', native: 'Mizo ṭawng', flag: '🌸', greeting: 'Chibai! Dam takin lo awm rawh le. I him e.' },
      { code: 'bod', name: 'Bodo', native: 'बड़ो', flag: '🌾', greeting: 'गोजोनथों! नोंथांखौ बरायबाय। नोंथाङा रैखाथि गोनां।' },
      { code: 'garo', name: 'Garo', native: 'A·chik', flag: '🏔️', greeting: 'Salam! Remember It-ona rimchaksoa. Na·a nambee dongenga.' }
    ];

    this.translations = {
      en: {
        app_name: "Remember It",
        patient_mode: "Patient View",
        caregiver_mode: "Caregiver View",
        daily_medicine: "Daily Medicines",
        brain_activities: "Memory Match Game",
        family_album: "My Loved Ones",
        sos_button: "EMERGENCY HELP (SOS)",
        select_language: "Select Language",
        tap_to_listen: "Tap to Listen",
        welcome_greeting: "Welcome! You are safe and loved.",
        add_medication: "Add New Medication",
        score_trend: "7-Day Cognitive Score Trend"
      }
    };

    this.medications = [
      { id: 1, name: "Donepezil (5mg)", time: "Morning (08:00 AM)", purpose: "Memory & Cognitive Care", taken: true, icon: "💊" },
      { id: 2, name: "Amlodipine (5mg)", time: "Afternoon (01:00 PM)", purpose: "Blood Pressure Control", taken: false, icon: "🩺" },
      { id: 3, name: "Vitamin B-Complex", time: "Evening (07:30 PM)", purpose: "Nerve & General Health", taken: false, icon: "🌿" }
    ];

    this.familyMembers = [
      { id: 1, name: "Sunita Hazarika", relation: "Wife (48 Years Together)", avatar: "👵", color: "#E9D5FF", speech: "This is Sunita, your beloved wife of 48 years. You are safe together at home." },
      { id: 2, name: "Rohit Hazarika", relation: "Son (Working in Guwahati)", avatar: "👨‍💼", color: "#BFDBFE", speech: "This is your son Rohit. He loves you very much and calls every afternoon." },
      { id: 3, name: "Ananya Barua", relation: "Daughter (Family Caregiver)", avatar: "👩‍⚕️", color: "#FEF08A", speech: "This is your daughter Ananya. She prepared your evening tea and medicines." },
      { id: 4, name: "Meera", relation: "Granddaughter (Age 8)", avatar: "👧", color: "#FED7AA", speech: "This is your sweet granddaughter Meera. She is drawing pictures for you." }
    ];

    this.cognitiveDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    this.cognitiveScores = [75, 82, 88, 78, 90, 85, 92];

    // Memory Game State
    this.memoryCards = [];
    this.flippedCards = [];
    this.matchedPairs = 0;
    this.moves = 0;

    this.init();
  }

  async init() {
    this.initClock();
    this.renderLanguageModal();
    await this.loadLanguage(this.currentLang);
    this.renderMedications();
    this.renderFamilyAlbum();
    this.initMemoryGame();
    this.renderCognitiveChart();
    this.bindEvents();

    // Fetch live data from Python API if available
    this.syncWithBackend();
  }

  // ── Sync with Python Flask API ───────────────────────────────────────────
  async syncWithBackend() {
    try {
      const res = await fetch('/api/medications');
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          this.medications = data;
          this.renderMedications();
        }
      }
    } catch (e) {
      // Offline fallback
    }

    try {
      const res = await fetch('/api/family');
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          this.familyMembers = data;
          this.renderFamilyAlbum();
        }
      }
    } catch (e) {}
  }

  // ── Live Clock & Date ────────────────────────────────────────────────────
  initClock() {
    const update = () => {
      const now = new Date();
      let hours = now.getHours();
      const mins = String(now.getMinutes()).padStart(2, '0');
      const ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12 || 12;

      const clockEl = document.getElementById('patientClock');
      if (clockEl) clockEl.textContent = `${hours}:${mins} ${ampm}`;

      const dateEl = document.getElementById('patientDate');
      if (dateEl) {
        const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
        dateEl.textContent = now.toLocaleDateString('en-US', options);
      }
    };
    update();
    setInterval(update, 1000);
  }

  // ── Text-to-Speech Engine ────────────────────────────────────────────────
  speak(text, langCode = this.currentLang) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.88; // Gentle and clear for elderly
    utterance.pitch = 1.0;

    const langMap = {
      en: 'en-IN',
      hi: 'hi-IN',
      as: 'as-IN',
      mni: 'hi-IN',
      kha: 'en-IN',
      lus: 'en-IN',
      bod: 'hi-IN',
      garo: 'en-IN'
    };

    utterance.lang = langMap[langCode] || 'en-IN';
    window.speechSynthesis.speak(utterance);
  }

  // ── Language & Localization ──────────────────────────────────────────────
  async loadLanguage(langCode) {
    this.currentLang = langCode;
    localStorage.setItem('ner_lang', langCode);

    // Update Language Trigger Button Label
    const langObj = this.languages.find(l => l.code === langCode) || this.languages[0];
    const triggerLabel = document.getElementById('currentLangLabel');
    if (triggerLabel) {
      triggerLabel.textContent = `${langObj.flag} ${langObj.native}`;
    }

    // Try fetching from Python Flask API
    try {
      const res = await fetch(`/api/translations/${langCode}`);
      if (res.ok) {
        this.translations[langCode] = await res.json();
      }
    } catch (e) {
      // Fallback
    }

    this.applyTranslations();
  }

  applyTranslations() {
    const dict = this.translations[this.currentLang] || this.translations['en'] || {};

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });

    const langObj = this.languages.find(l => l.code === this.currentLang) || this.languages[0];
    const greetingSub = document.getElementById('greetingSubtitle');
    if (greetingSub) {
      greetingSub.textContent = langObj.greeting;
    }
  }

  renderLanguageModal() {
    const grid = document.getElementById('langGrid');
    if (!grid) return;

    grid.innerHTML = this.languages.map(lang => `
      <button class="lang-card-btn ${lang.code === this.currentLang ? 'active' : ''}" data-lang="${lang.code}">
        <span class="lang-flag">${lang.flag}</span>
        <div class="lang-names">
          <strong>${lang.native}</strong>
          <span>${lang.name}</span>
        </div>
      </button>
    `).join('');

    grid.querySelectorAll('.lang-card-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const selected = btn.getAttribute('data-lang');
        this.loadLanguage(selected);
        this.closeModal('langModal');
        this.sound.playClick();
        this.showToast(`Language set to ${btn.querySelector('strong').textContent}`);
      });
    });
  }

  // ── Medications Rendering & Toggling ─────────────────────────────────────
  renderMedications() {
    // 1. Patient Simple List
    const patientList = document.getElementById('patientMedsList');
    if (patientList) {
      patientList.innerHTML = this.medications.map(med => `
        <div class="med-card-simple ${med.taken ? 'taken' : ''}">
          <div class="med-info-box">
            <div class="med-icon-box">${med.icon || '💊'}</div>
            <div>
              <div class="med-title">${med.name}</div>
              <div class="med-subtitle">${med.time} • ${med.purpose}</div>
            </div>
          </div>
          <button class="btn-med-toggle ${med.taken ? 'taken' : 'pending'}" data-id="${med.id}">
            <span>${med.taken ? '✅ Taken' : '⏳ Tap When Taken'}</span>
          </button>
        </div>
      `).join('');

      patientList.querySelectorAll('.btn-med-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = parseInt(btn.getAttribute('data-id'), 10);
          this.toggleMedication(id);
        });
      });
    }

    // 2. Caregiver Table
    const caregiverList = document.getElementById('caregiverMedsTable');
    if (caregiverList) {
      caregiverList.innerHTML = this.medications.map(med => `
        <div class="caregiver-med-row">
          <div>
            <strong>${med.name}</strong>
            <div style="font-size: 0.85rem; color: var(--text-muted);">${med.time} — ${med.purpose}</div>
          </div>
          <button class="btn-med-toggle ${med.taken ? 'taken' : 'pending'}" data-id="${med.id}">
            <span>${med.taken ? '✅ Taken' : '⏳ Pending'}</span>
          </button>
        </div>
      `).join('');

      caregiverList.querySelectorAll('.btn-med-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = parseInt(btn.getAttribute('data-id'), 10);
          this.toggleMedication(id);
        });
      });
    }

    // Summary badge
    const pendingCount = this.medications.filter(m => !m.taken).length;
    const summaryEl = document.getElementById('medsStatusSummary');
    if (summaryEl) {
      summaryEl.textContent = pendingCount === 0 ? 'All doses taken today! 🌸' : `${pendingCount} pending today`;
    }
  }

  async toggleMedication(id) {
    const med = this.medications.find(m => m.id === id);
    if (!med) return;

    med.taken = !med.taken;
    this.sound.playClick();
    if (med.taken) {
      this.sound.playChime();
      this.showToast(`Marked ${med.name} as taken! ✅`);
    } else {
      this.showToast(`Marked ${med.name} as pending.`);
    }

    this.renderMedications();

    // Call Python API
    try {
      await fetch(`/api/medications/${id}/toggle`, { method: 'POST' });
    } catch (e) {}
  }

  // ── 3D Physics Flip Cards Brain Game ─────────────────────────────────────
  initMemoryGame() {
    const items = [
      { id: 1, emoji: '🦏', title: 'One-Horned Rhino' },
      { id: 2, emoji: '🍵', title: 'Assam Green Tea' },
      { id: 3, emoji: '🦌', title: 'Sangai Deer' },
      { id: 4, emoji: '🌉', title: 'Root Bridge' },
      { id: 5, emoji: '🌸', title: 'Anthurium Flower' },
      { id: 6, emoji: '🥁', title: 'Bihu Dhol' }
    ];

    // Duplicate for pairs and shuffle
    const deck = [...items, ...items].map((item, idx) => ({
      ...item,
      uniqueId: idx
    }));

    // Fisher-Yates shuffle
    for (let i = deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [deck[i], deck[j]] = [deck[j], deck[i]];
    }

    this.memoryCards = deck;
    this.flippedCards = [];
    this.matchedPairs = 0;
    this.moves = 0;

    this.renderMemoryGame();
  }

  renderMemoryGame() {
    const grid = document.getElementById('memoryGrid');
    const movesEl = document.getElementById('gameMoves');
    const matchesEl = document.getElementById('gameMatches');
    if (!grid) return;

    if (movesEl) movesEl.textContent = `Moves: ${this.moves}`;
    if (matchesEl) matchesEl.textContent = `Matches: ${this.matchedPairs}/6`;

    grid.innerHTML = this.memoryCards.map((card, idx) => `
      <div class="memory-card" data-idx="${idx}">
        <div class="card-front"></div>
        <div class="card-back">
          <span class="card-emoji">${card.emoji}</span>
          <span class="card-title">${card.title}</span>
        </div>
      </div>
    `).join('');

    grid.querySelectorAll('.memory-card').forEach(el => {
      el.addEventListener('click', () => {
        const idx = parseInt(el.getAttribute('data-idx'), 10);
        this.flipMemoryCard(idx, el);
      });
    });
  }

  flipMemoryCard(idx, el) {
    if (this.flippedCards.length >= 2 || el.classList.contains('flipped') || el.classList.contains('matched')) {
      return;
    }

    this.sound.playClick();
    el.classList.add('flipped');
    this.flippedCards.push({ idx, card: this.memoryCards[idx], el });

    if (this.flippedCards.length === 2) {
      this.moves++;
      const movesEl = document.getElementById('gameMoves');
      if (movesEl) movesEl.textContent = `Moves: ${this.moves}`;

      const [first, second] = this.flippedCards;
      if (first.card.id === second.card.id) {
        // Match!
        setTimeout(() => {
          first.el.classList.add('matched');
          second.el.classList.add('matched');
          this.matchedPairs++;
          const matchesEl = document.getElementById('gameMatches');
          if (matchesEl) matchesEl.textContent = `Matches: ${this.matchedPairs}/6`;
          this.flippedCards = [];
          this.sound.playChime();

          if (this.matchedPairs === 6) {
            setTimeout(() => {
              this.sound.playFanfare();
              this.showToast('🎉 Wonderful job! All memory pairs matched!');
              this.speak('Wonderful job! You completed all the memory matches!');
              // Record score to Python backend
              fetch('/api/scores', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ score: 95, moves: this.moves, day: 'Today' })
              }).catch(() => {});
            }, 300);
          }
        }, 350);
      } else {
        // No match - smooth physics flip back
        setTimeout(() => {
          first.el.classList.remove('flipped');
          second.el.classList.remove('flipped');
          this.flippedCards = [];
        }, 900);
      }
    }
  }

  // ── Family Reminiscence Album ─────────────────────────────────────────────
  renderFamilyAlbum() {
    const grid = document.getElementById('familyAlbumGrid');
    if (!grid) return;

    grid.innerHTML = this.familyMembers.map(member => `
      <div class="family-member-card" data-speech="${member.speech}">
        <div class="family-avatar-circle" style="background-color: ${member.color || '#E8F5F2'};">
          ${member.avatar}
        </div>
        <div class="family-name">${member.name}</div>
        <div class="family-relation">${member.relation}</div>
        <button class="btn-hear-voice">
          <span>🔊</span> Listen
        </button>
      </div>
    `).join('');

    grid.querySelectorAll('.family-member-card').forEach(card => {
      card.addEventListener('click', () => {
        const speech = card.getAttribute('data-speech');
        this.sound.playClick();
        this.speak(speech);
        this.showToast(`Playing voice memory...`);
      });
    });
  }

  // ── 7-Day Cognitive Chart ────────────────────────────────────────────────
  renderCognitiveChart() {
    const svg = document.getElementById('cognitiveChart');
    if (!svg) return;

    const width = 500;
    const height = 180;
    const padX = 35;
    const padY = 25;
    const usableW = width - padX * 2;
    const usableH = height - padY * 2;

    const minScore = 60;
    const maxScore = 100;

    const points = this.cognitiveScores.map((score, i) => {
      const x = padX + (i / (this.cognitiveScores.length - 1)) * usableW;
      const y = height - padY - ((score - minScore) / (maxScore - minScore)) * usableH;
      return { x, y, score, day: this.cognitiveDays[i] };
    });

    const pathD = points.reduce((acc, p, i) => {
      return i === 0 ? `M ${p.x} ${p.y}` : `${acc} L ${p.x} ${p.y}`;
    }, '');

    const areaD = `${pathD} L ${points[points.length - 1].x} ${height - padY} L ${points[0].x} ${height - padY} Z`;

    svg.innerHTML = `
      <defs>
        <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#2E7D6E" stop-opacity="0.25"/>
          <stop offset="100%" stop-color="#2E7D6E" stop-opacity="0.0"/>
        </linearGradient>
      </defs>
      <!-- Grid line -->
      <line x1="${padX}" y1="${height - padY}" x2="${width - padX}" y2="${height - padY}" stroke="#D8E2DF" stroke-width="1.5"/>
      <path class="chart-area" d="${areaD}"/>
      <path class="chart-path" d="${pathD}"/>
      ${points.map(p => `
        <circle class="chart-dot" cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}">
          <title>${p.day}: ${p.score} / 100</title>
        </circle>
      `).join('')}
    `;

    const daysEl = document.getElementById('chartDays');
    if (daysEl) {
      daysEl.innerHTML = this.cognitiveDays.map((d, i) => `
        <span style="${i === this.cognitiveDays.length - 1 ? 'color: var(--primary); font-weight:800;' : ''}">${d}</span>
      `).join('');
    }
  }

  // ── Mode Switcher (Patient vs Caregiver) ──────────────────────────────────
  switchMode(mode) {
    this.currentMode = mode;
    this.sound.playClick();

    const patientBtn = document.getElementById('btnModePatient');
    const caregiverBtn = document.getElementById('btnModeCaregiver');
    const patientView = document.getElementById('patientView');
    const caregiverView = document.getElementById('caregiverView');

    if (mode === 'patient') {
      patientBtn?.classList.add('active');
      caregiverBtn?.classList.remove('active');
      if (patientView) patientView.style.display = 'flex';
      if (caregiverView) caregiverView.style.display = 'none';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      caregiverBtn?.classList.add('active');
      patientBtn?.classList.remove('active');
      if (patientView) patientView.style.display = 'none';
      if (caregiverView) caregiverView.style.display = 'flex';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  // ── Toast Messages ───────────────────────────────────────────────────────
  showToast(msg) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2800);
  }

  // ── Modals Helper ────────────────────────────────────────────────────────
  openModal(id) {
    const m = document.getElementById(id);
    if (m) {
      m.classList.add('active');
      m.setAttribute('aria-hidden', 'false');
    }
  }

  closeModal(id) {
    const m = document.getElementById(id);
    if (m) {
      m.classList.remove('active');
      m.setAttribute('aria-hidden', 'true');
    }
  }

  // ── Event Bindings ───────────────────────────────────────────────────────
  bindEvents() {
    // Mode switcher buttons
    document.getElementById('btnModePatient')?.addEventListener('click', () => this.switchMode('patient'));
    document.getElementById('btnModeCaregiver')?.addEventListener('click', () => this.switchMode('caregiver'));

    // Language selector trigger
    document.getElementById('btnLangSelect')?.addEventListener('click', () => {
      this.sound.playClick();
      this.openModal('langModal');
    });
    document.getElementById('btnCloseLangModal')?.addEventListener('click', () => {
      this.closeModal('langModal');
    });

    // Speak greeting
    document.getElementById('btnSpeakGreeting')?.addEventListener('click', () => {
      this.sound.playClick();
      const langObj = this.languages.find(l => l.code === this.currentLang) || this.languages[0];
      this.speak(langObj.greeting);
      this.showToast('Speaking greeting...');
    });

    // Mute toggle
    document.getElementById('btnMuteToggle')?.addEventListener('click', (e) => {
      this.sound.muted = !this.sound.muted;
      e.currentTarget.textContent = this.sound.muted ? '🔇' : '🔊';
      this.showToast(this.sound.muted ? 'Sound Muted' : 'Sound Enabled');
    });

    // Restart Memory Game
    document.getElementById('btnRestartGame')?.addEventListener('click', () => {
      this.initMemoryGame();
      this.sound.playClick();
      this.showToast('Memory game restarted!');
    });

    // Emergency SOS Trigger
    document.getElementById('btnFloatingSos')?.addEventListener('click', () => {
      this.sound.playSiren();
      this.openModal('sosModal');
      this.speak('Emergency alert activated. Calling family and emergency services.');
      fetch('/api/sos', { method: 'POST' }).catch(() => {});
    });

    document.getElementById('btnCloseSosModal')?.addEventListener('click', () => {
      this.closeModal('sosModal');
    });

    // Caregiver: Add Medicine
    document.getElementById('btnAddMedModalOpen')?.addEventListener('click', () => {
      this.sound.playClick();
      this.openModal('addMedModal');
    });
    document.getElementById('btnCloseAddMed')?.addEventListener('click', () => {
      this.closeModal('addMedModal');
    });
    document.getElementById('btnCancelAddMed')?.addEventListener('click', () => {
      this.closeModal('addMedModal');
    });

    document.getElementById('formAddMed')?.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('inputMedName').value.trim();
      const time = document.getElementById('inputMedTime').value;
      const purpose = document.getElementById('inputMedPurpose').value.trim();

      if (!name) return;

      const newMed = {
        id: Date.now(),
        name,
        time,
        purpose: purpose || 'Daily Prescribed Care',
        taken: false,
        icon: '💊'
      };

      this.medications.push(newMed);
      this.renderMedications();
      this.closeModal('addMedModal');
      document.getElementById('formAddMed').reset();
      this.sound.playChime();
      this.showToast(`Added ${name} to schedule!`);

      // Post to Python backend
      fetch('/api/medications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newMed)
      }).catch(() => {});
    });
  }
}

// ── Instantiate Application on Page Load ────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  window.dementiaApp = new DementiaCareApp();
});
