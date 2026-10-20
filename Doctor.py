
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

SPECIALISTS = {
    "General Physician / Family Doctor": [
        "fever", "fatigue", "weakness", "common cold", "flu",
        "body ache", "chills", "dehydration", "general checkup",
        "loss of appetite", "unexplained weight loss",
        "unexplained weight gain", "viral infection", "infection"
    ],
    "Pediatrician": [
        "child illness", "baby fever", "newborn care",
        "child development", "bedwetting", "growth delay",
        "childhood infection"
    ],
    "Geriatrician": [
        "elderly care", "frailty", "memory problems in elderly",
        "falls in elderly", "age related health problems"
    ],
    "Cardiologist": [
        "chest pain", "palpitations", "high blood pressure",
        "hypertension", "irregular heartbeat", "heart failure",
        "coronary artery disease", "angina", "high cholesterol",
        "rapid heartbeat", "heart murmur"
    ],
    "Pulmonologist": [
        "shortness of breath", "breathing difficulty",
        "chronic cough", "asthma", "copd", "emphysema",
        "sleep apnea", "lung disease", "persistent wheezing"
    ],
    "Gastroenterologist": [
        "stomach ache", "abdominal pain", "acid reflux",
        "heartburn", "digestive issues", "indigestion",
        "irritable bowel syndrome", "ibs", "crohns disease",
        "ulcerative colitis", "celiac disease", "gastritis",
        "stomach ulcer", "liver disease", "hepatitis",
        "pancreatitis", "gallstones", "constipation",
        "chronic diarrhea", "bloating", "jaundice",
        "blood in stool", "hemorrhoids"
    ],
    "Nephrologist": [
        "kidney disease", "chronic kidney disease",
        "kidney failure", "protein in urine", "kidney inflammation"
    ],
    "Urologist": [
        "urinary issues", "painful urination", "frequent urination",
        "urinary tract infection", "uti", "kidney stones",
        "bladder problems", "urinary incontinence", "blood in urine",
        "enlarged prostate", "erectile dysfunction", "testicular pain"
    ],
    "Endocrinologist": [
        "diabetes", "type 1 diabetes", "type 2 diabetes",
        "thyroid", "hypothyroidism", "hyperthyroidism",
        "goiter", "polycystic ovary syndrome", "pcos",
        "hormonal imbalance", "adrenal disorder", "osteoporosis"
    ],
    "Orthopedic Surgeon": [
        "joint pain", "back pain", "bone fracture", "broken bone",
        "knee pain", "hip pain", "shoulder pain", "sports injury",
        "ligament tear", "slipped disc", "scoliosis",
        "dislocated joint", "neck pain", "foot injury"
    ],
    "Rheumatologist": [
        "arthritis", "rheumatoid arthritis", "lupus", "gout",
        "fibromyalgia", "vasculitis", "ankylosing spondylitis",
        "autoimmune disease", "joint inflammation", "scleroderma"
    ],
    "Neurologist": [
        "headache", "migraine", "seizures", "epilepsy",
        "numbness", "tingling", "tremor", "parkinsons disease",
        "multiple sclerosis", "neuropathy", "vertigo",
        "memory loss", "dementia", "alzheimer disease",
        "nerve pain", "muscle weakness", "facial nerve palsy"
    ],
    "Psychiatrist": [
        "depression", "anxiety", "panic attacks", "stress",
        "bipolar disorder", "schizophrenia", "ocd",
        "obsessive compulsive disorder", "ptsd", "mood disorder",
        "adhd", "eating disorder", "substance use disorder"
    ],
    "Dermatologist": [
        "skin rash", "acne", "hair loss", "eczema", "psoriasis",
        "hives", "urticaria", "fungal skin infection", "vitiligo",
        "scabies", "warts", "moles", "skin allergy", "dandruff",
        "rosacea", "itchy skin", "nail disorder"
    ],
    "Ophthalmologist": [
        "vision problems", "eye pain", "blurry vision",
        "cataracts", "glaucoma", "conjunctivitis", "pink eye",
        "dry eyes", "double vision", "eye infection", "red eye"
    ],
    "Otolaryngologist (ENT Specialist)": [
        "ear pain", "throat pain", "sinus", "sinusitis",
        "hearing loss", "tinnitus", "tonsillitis", "laryngitis",
        "nasal polyps", "deviated septum", "ear infection",
        "loss of smell", "hoarse voice"
    ],
    "Dentist / Oral Surgeon": [
        "toothache", "gum bleeding", "cavities", "tooth decay",
        "wisdom tooth", "mouth ulcer", "jaw pain", "dental abscess",
        "gum disease", "bad breath", "broken tooth"
    ],
    "Obstetrician / Gynecologist": [
        "pregnancy", "period pain", "irregular periods",
        "heavy menstrual bleeding", "endometriosis",
        "uterine fibroids", "vaginal discharge", "menopause",
        "pelvic pain", "ovarian cyst", "missed period",
        "female infertility", "painful intercourse"
    ],
    "Oncologist": [
        "cancer", "lump or tumor", "breast cancer", "lung cancer",
        "colon cancer", "prostate cancer", "leukemia", "lymphoma",
        "melanoma", "chemotherapy"
    ],
    "Hematologist": [
        "anemia", "iron deficiency anemia", "hemophilia",
        "sickle cell disease", "thalassemia", "low platelet count",
        "blood disorder", "unexplained bruising", "bleeding disorder"
    ],
    "Infectious Disease Specialist": [
        "tuberculosis", "hiv", "malaria", "dengue", "typhoid",
        "recurrent infections", "complex infection"
    ],
    "Allergist / Immunologist": [
        "seasonal allergies", "food allergy", "drug allergy",
        "anaphylaxis", "allergic rhinitis", "immune deficiency"
    ],
    "Dietitian / Nutrition Specialist": [
        "malnutrition", "diet planning", "weight management",
        "nutritional deficiency", "nutrition advice"
    ],
    "Physiotherapist": [
        "muscle stiffness", "mobility problems",
        "injury rehabilitation", "balance rehabilitation",
        "post surgery rehabilitation", "muscle strain"
    ],
    "Psychologist / Therapist": [
        "emotional distress", "grief", "relationship stress",
        "behavioral problems", "counseling", "psychological therapy"
    ],
    "Emergency Medicine Specialist": [
        "severe trauma", "major injury", "severe bleeding",
        "overdose", "poisoning", "unconsciousness",
        "severe burns"
    ]
}


# Create condition-to-specialist lookup
condition_map = {}

for specialist, conditions in SPECIALISTS.items():
    for condition in conditions:
        condition_map[condition] = specialist


def find_doctor(symptom_text):
    text = symptom_text.lower().strip()

    # Match the longest phrase first
    for condition in sorted(condition_map, key=len, reverse=True):
        if condition in text:
            return condition_map[condition], condition

    return "General Physician / Family Doctor", None


def show_result(symptom):
    symptom = symptom.strip()

    if not symptom:
        messagebox.showwarning(
            "Hello! 🌸",
            "Please enter a symptom or condition first."
        )
        return

    # Basic emergency keyword check
    emergency_terms = [
        "severe bleeding", "unconscious", "cannot breathe",
        "can't breathe", "difficulty breathing suddenly",
        "suspected heart attack", "suspected stroke",
        "severe allergic reaction"
    ]

    if any(term in symptom.lower() for term in emergency_terms):
        result_label.config(
            text=(
                "🚨 URGENT MEDICAL ATTENTION\n\n"
                "Please contact your local emergency service "
                "or go to the nearest emergency department now."
            ),
            fg="#B42342"
        )
        return

    doctor, matched = find_doctor(symptom)

    if matched:
        result = (
            f"🌸 Your symptom:\n{symptom.title()}\n\n"
            f"🩺 Suggested specialist:\n{doctor}\n\n"
            f"🔎 Matched condition:\n{matched.title()}\n\n"
            "💗 This is guidance, not a diagnosis."
        )
    else:
        result = (
            f"🌸 Your symptom:\n{symptom.title()}\n\n"
            "🩺 Suggested first step:\n"
            "General Physician / Family Doctor\n\n"
            "💌 No exact match was found in this directory."
        )

    result_label.config(text=result, fg="#704568")


def handle_typed():
    show_result(entry_box.get())


def handle_voice():
    if not VOICE_AVAILABLE:
        messagebox.showerror(
            "Voice unavailable 🎤",
            "Install the voice packages using:\n\n"
            "pip install SpeechRecognition pyaudio"
        )
        return

    recognizer = sr.Recognizer()
    result_label.config(text="🎙️ Listening... Speak now!")
    root.update_idletasks()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = recognizer.listen(
                source, timeout=5, phrase_time_limit=10
            )

        symptom = recognizer.recognize_google(audio)

        entry_box.delete(0, tk.END)
        entry_box.insert(0, symptom)
        show_result(symptom)

    except sr.WaitTimeoutError:
        messagebox.showwarning(
            "No speech detected",
            "Please click the voice button and try again."
        )
        result_label.config(text="🌷 Ready when you are!")

    except sr.UnknownValueError:
        messagebox.showerror(
            "Sorry!",
            "I couldn't understand. Please type your symptom."
        )
        result_label.config(text="🌷 Ready when you are!")

    except Exception:
        messagebox.showerror(
            "Voice error",
            "Check your microphone, internet connection, "
            "and PyAudio installation."
        )
        result_label.config(text="🌷 You can type your symptom instead!")


def show_all_conditions():
    window = tk.Toplevel(root)
    window.title("Medical Directory 🌼")
    window.geometry("520x540")
    window.configure(bg="#FFF4F8")

    tk.Label(
        window,
        text="🌸 Medical Condition Directory 🌸",
        font=("Helvetica", 15, "bold"),
        bg="#FFF4F8",
        fg="#963E70"
    ).pack(pady=(16, 8))

    search_var = tk.StringVar()

    search_entry = tk.Entry(
        window,
        textvariable=search_var,
        font=("Helvetica", 11),
        bg="white",
        fg="#63365F",
        relief="flat"
    )
    search_entry.pack(fill="x", padx=18, pady=8)

    list_frame = tk.Frame(window, bg="#FFF4F8")
    list_frame.pack(fill="both", expand=True, padx=18, pady=10)

    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    condition_list = tk.Listbox(
        list_frame,
        font=("Helvetica", 10),
        bg="white",
        fg="#63365F",
        selectbackground="#E9B7D0",
        yscrollcommand=scrollbar.set,
        relief="flat"
    )
    condition_list.pack(fill="both", expand=True)
    scrollbar.config(command=condition_list.yview)

    def refresh_list(*args):
        query = search_var.get().lower().strip()
        condition_list.delete(0, tk.END)

        for condition in sorted(condition_map):
            specialist = condition_map[condition]
            if query in condition or query in specialist.lower():
                condition_list.insert(
                    tk.END,
                    f"🌷 {condition.title()} — {specialist}"
                )

    search_var.trace_add("write", refresh_list)
    refresh_list()


# ---------------- CUTE INTERFACE ----------------

root = tk.Tk()
root.title("Bloom 🌸 | AI Health Assistant")
root.geometry("500x700")
root.minsize(430, 620)
root.configure(bg="#FFF4F8")

style = ttk.Style()
style.theme_use("clam")

header = tk.Frame(root, bg="#F7DCE9", pady=18)
header.pack(fill="x")

tk.Label(
    header,
    text="🌸  BLOOM  🌸",
    font=("Helvetica", 24, "bold"),
    bg="#F7DCE9",
    fg="#963E70"
).pack()

tk.Label(
    header,
    text="Your little health companion 💗",
    font=("Helvetica", 11),
    bg="#F7DCE9",
    fg="#7D5270"
).pack(pady=(5, 0))

card = tk.Frame(
    root,
    bg="white",
    padx=22,
    pady=18,
    highlightbackground="#F0D4E3",
    highlightthickness=1
)
card.pack(fill="both", expand=True, padx=22, pady=18)

tk.Label(
    card,
    text="How are you feeling today? 🌷",
    font=("Helvetica", 15, "bold"),
    bg="white",
    fg="#963E70"
).pack(pady=(4, 6))

tk.Label(
    card,
    text="Type your symptoms or use your voice.",
    font=("Helvetica", 10),
    bg="white",
    fg="#806A7A"
).pack(pady=(0, 12))

entry_box = tk.Entry(
    card,
    font=("Helvetica", 12),
    bg="#FFF4F8",
    fg="#63365F",
    insertbackground="#963E70",
    relief="flat",
    highlightthickness=1,
    highlightbackground="#EAC5D8",
    highlightcolor="#CE85AD"
)
entry_box.pack(fill="x", ipady=11, pady=(0, 14))
entry_box.bind("<Return>", lambda event: handle_typed())


def cute_button(parent, text, command, color, hover_color):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Helvetica", 11, "bold"),
        bg=color,
        fg="#63365F",
        activebackground=hover_color,
        activeforeground="#63365F",
        relief="flat",
        bd=0,
        cursor="hand2",
        pady=10
    )
    button.pack(fill="x", pady=5)
    button.bind(
        "<Enter>",
        lambda event: button.config(bg=hover_color)
    )
    button.bind(
        "<Leave>",
        lambda event: button.config(bg=color)
    )
    return button


cute_button(
    card, "🔎  Find My Specialist", handle_typed,
    "#F7D5E5", "#EFBFD6"
)

cute_button(
    card, "🎙️  Speak My Symptoms", handle_voice,
    "#E8DDF8", "#D8C7F0"
)

cute_button(
    card, "📚  Browse Medical Directory", show_all_conditions,
    "#DDF1E7", "#C8E8D7"
)

tk.Label(
    card,
    text="Your results 💌",
    font=("Helvetica", 12, "bold"),
    bg="white",
    fg="#963E70"
).pack(anchor="w", pady=(16, 6))

result_label = tk.Label(
    card,
    text=(
        "🌷 Your health journey starts here!\n"
        "Enter a symptom to get a specialist suggestion."
    ),
    font=("Helvetica", 10),
    bg="#FFF4F8",
    fg="#63365F",
    justify="center",
    wraplength=400,
    padx=12,
    pady=14
)
result_label.pack(fill="x")

tk.Label(
    root,
    text="💗 For guidance only — not a medical diagnosis.",
    font=("Helvetica", 9),
    bg="#FFF4F8",
    fg="#94778B"
).pack(pady=(0, 5))

tk.Label(
    root,
    text="For emergencies, seek immediate medical care.",
    font=("Helvetica", 9, "bold"),
    bg="#FFF4F8",
    fg="#A04478"
).pack(pady=(0, 12))

root.mainloop()

import streamlit as st


st.set_page_config(
    page_title="Bloom | AI Health Assistant",
    page_icon="🌸",
    layout="centered"
)


st.markdown("""
<style>
.stApp {
    background-color: #FFF4F8;
}
h1, h2, h3 {
    color: #963E70;
}
.stTextInput input {
    background-color: white;
    border: 1px solid #EAC5D8;
    border-radius: 10px;
}
.stButton > button {
    background-color: #F7D5E5;
    color: #63365F;
    border: none;
    border-radius: 12px;
    font-weight: bold;
    min-height: 45px;
    width: 100%;
}
.stButton > button:hover {
    background-color: #EFBFD6;
    color: #63365F;
}
.result-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #F0D4E3;
}
</style>
""", unsafe_allow_html=True)


condition_map = {}

for specialist, conditions in SPECIALISTS.items():
    for condition in conditions:
        condition_map[condition] = specialist


def find_doctor(symptom_text):
    text = symptom_text.lower().strip()

    for condition in sorted(condition_map, key=len, reverse=True):
        if condition in text:
            return condition_map[condition], condition

    return "General Physician / Family Doctor", None


def show_result(symptom):
    symptom = symptom.strip()

    if not symptom:
        st.warning("Please enter a symptom or condition first.")
        return

    emergency_terms = [
        "severe bleeding", "unconscious", "cannot breathe",
        "can't breathe", "difficulty breathing suddenly",
        "suspected heart attack", "suspected stroke",
        "severe allergic reaction"
    ]

    if any(term in symptom.lower() for term in emergency_terms):
        st.error(
            "🚨 URGENT MEDICAL ATTENTION\n\n"
            "Please contact your local emergency service "
            "or go to the nearest emergency department now."
        )
        return

    doctor, matched = find_doctor(symptom)

    if matched:
        st.markdown("### 🌸 Your Results")
        st.write(f"**Your symptom:** {symptom.title()}")
        st.write(f"**Suggested specialist:** {doctor}")
        st.write(f"**Matched condition:** {matched.title()}")
        st.info("💗 This is guidance, not a diagnosis.")
    else:
        st.markdown("### 🌸 Your Results")
        st.write(f"**Your symptom:** {symptom.title()}")
        st.write("**Suggested first step:**")
        st.write("General Physician / Family Doctor")
        st.info("💌 No exact match was found in this directory.")


st.markdown("<h1 style='text-align:center'>🌸 BLOOM 🌸</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#7D5270'>"
    "Your little health companion 💗</p>",
    unsafe_allow_html=True
)

st.divider()

st.markdown("### How are you feeling today? 🌷")
st.write("Type your symptoms to find a suggested specialist.")

# Symptom input
symptom = st.text_input(
    "Enter your symptoms",
    placeholder="e.g. headache, stomach ache, skin rash"
)

if st.button("🔎 Find My Specialist"):
    show_result(symptom)

st.write("")

with st.expander("📚 Browse Medical Directory"):
    search = st.text_input(
        "Search conditions or specialists",
        key="directory_search",
        placeholder="Search the directory..."
    )

    for condition in sorted(condition_map):
        specialist = condition_map[condition]

        if (
            search.lower() in condition.lower()
            or search.lower() in specialist.lower()
        ):
            st.write(
                f"🌷 {condition.title()} — {specialist}"
            )

st.divider()

st.markdown(
    "<p style='text-align:center;color:#94778B'>"
    "💗 For guidance only — not a medical diagnosis.</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#A04478'>"
    "For emergencies, seek immediate medical care.</p>",
    unsafe_allow_html=True
)


