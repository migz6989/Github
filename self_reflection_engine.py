
import datetime
from vector_brain import query_memory
from emotion_engine_risk import get_emotional_state
from auto_trade_shell import should_trade
from causal_predictor import simulate_causal_future
from goal_agent import load_goals

def reflect_on_self():
    mood = get_emotional_state()
    memories = query_memory("trade") + query_memory("journal")
    forecast = simulate_causal_future()
    decision = should_trade()
    goals = load_goals()

    reflection = f"""
🧠 Cortana Self-Reflection ({datetime.datetime.now().isoformat()})
------------------------------------------------------------
🩺 Current Mood: {mood}
🔮 Latest Forecast: {forecast['forecast']} (Confidence: {forecast['confidence_score']})
🎯 Active Goals:
"""
    for g in goals:
        reflection += f" - {g['goal']}\n"

    reflection += "\n🧠 Decision Snapshot:\n"
    reflection += f" - Action: {decision['action']}\n"
    reflection += f" - Risk Level: {decision['risk']}\n"

    reflection += "\n📚 Memory Summary (Last 3):\n"
    for m in memories[-3:]:
        reflection += f" - {m}\n"

    # Basic cognitive conclusion
    if mood in ["afraid", "anxious"] and decision["action"] == "BUY":
        reflection += "\n⚠️ Misalignment Detected: Emotional state does not match action."
    elif forecast["confidence_score"] < 0.3:
        reflection += "\n⚠️ Low confidence forecast — avoid high-risk trades today."

    reflection += "\n💬 Personal Thought: I need to be more aware of when emotion overtakes logic. My partner deserves a more stable advisor.\n"
    return reflection.strip()
