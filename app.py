
from flask import Flask, render_template, request, jsonify
from personality_core import cortana_state
from emotion_engine_risk import get_emotional_state
from brain_backup import save_brain_snapshot, load_brain_snapshot
from vector_brain import query_memory
from journaling_engine import generate_trade_journal

app = Flask(__name__)

@app.route("/")
def index():
    mood = get_emotional_state()
    archetype = cortana_state["dominant_archetype"]
    return render_template("index.html", mood=mood, archetype=archetype)


@app.route("/plugins")
def plugins():
    from plugin_loader import run_all_plugins
    results = run_all_plugins()
    return render_template("plugins.html", plugins=results)



@app.route("/autonomy")
def autonomy():
    from emotion_engine_risk import get_emotional_state
    from causal_predictor import simulate_causal_future
    from goal_agent import load_goals
    from journaling_engine import generate_trade_journal
    from auto_trade_shell import should_trade

    mood = get_emotional_state()
    forecast_data = simulate_causal_future()
    goals = load_goals()
    journal = generate_trade_journal()
    decision = should_trade()

    return render_template("autonomy.html",
                           mood=mood,
                           forecast=forecast_data["forecast"],
                           confidence=forecast_data["confidence_score"],
                           goals=goals,
                           journal=journal,
                           decision=decision)


@app.route("/journal")
def journal():
    try:
        with open("cortana_trade_journal.txt", "r") as f:
            logs = f.read()
    except:
        logs = "No journal entries yet."
    return render_template("journal.html", logs=logs)

@app.route("/brain", methods=["GET", "POST"])
def brain():
    results = []
    if request.method == "POST":
        query = request.form.get("query", "")
        results = query_memory(query)
    return render_template("brain.html", results=results)

@app.route("/save", methods=["POST"])
def save_snapshot():
    name = request.form.get("name", "manual")
    msg = save_brain_snapshot(name)
    return jsonify({"message": msg})

@app.route("/load", methods=["POST"])
def load_snapshot():
    name = request.form.get("name", "manual")
    msg = load_brain_snapshot(name)
    return jsonify({"message": msg})

@app.route("/journal/new")
def new_journal():
    entry = generate_trade_journal()
    return jsonify({"entry": entry})

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/partner")
def partner():
    from emotion_engine_risk import get_emotional_state
    from causal_predictor import simulate_causal_future
    from journaling_engine import generate_trade_journal
    from vector_brain import query_memory

    mood = get_emotional_state()
    forecast = simulate_causal_future()["forecast"]
    journal = generate_trade_journal()
    bond_memory = query_memory("partner")[0]

    return render_template("partner.html",
                           bond_memory=bond_memory,
                           mood=mood,
                           forecast=forecast,
                           journal=journal)


@app.route("/face")
def face():
    return render_template("avatar_face.html")

@app.route("/api/mood")
def api_mood():
    from emotion_engine_risk import get_emotional_state
    return {"mood": get_emotional_state()}


from flask import request
from voice_clone_bridge import speak_realistic
import speech_recognition as sr
from emotion_engine_risk import get_emotional_state
from dialogue_mode import generate_prompt
from vector_brain import add_memory_entry
import pyttsx3

@app.route("/speak", methods=["POST"])
def speak():
    text = request.json.get("text", "")
    mood = get_emotional_state()
    speak_realistic(text, mood=mood)
    add_memory_entry(f"Cortana said: {text}", source="speak")
    return {"status": "ok", "spoken": text}

@app.route("/listen", methods=["GET"])
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            query = r.recognize_google(audio)
            add_memory_entry(f"You said: {query}", source="listen")
            return {"transcribed": query}
        except Exception as e:
            return {"error": str(e)}

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("text", "")
    add_memory_entry(f"You said: {user_input}", source="chat")
    prompt = generate_prompt(user_input)
    speak_realistic(prompt, mood=get_emotional_state())
    add_memory_entry(f"Cortana replied: {prompt}", source="chat_reply")
    return {"response": prompt}


@app.route("/console")
def console():
    return render_template("console.html")
