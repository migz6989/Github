
import random
from emotion_engine_risk import get_emotional_state
from plugin_loader import run_all_plugins

def simulate_causal_future():
    mood = get_emotional_state()
    plugins = run_all_plugins()

    risk_factor = random.uniform(0.0, 1.0)
    mood_bias = {
        "euphoric": 0.8,
        "confident": 0.7,
        "calm": 0.5,
        "anxious": 0.3,
        "afraid": 0.1
    }

    mood_influence = mood_bias.get(mood, 0.5)
    confidence = round((mood_influence + risk_factor) / 2, 2)

    forecast = "Market likely favorable for aggressive entry." if confidence > 0.6 else                "Caution advised — conditions unstable." if confidence > 0.4 else                "High risk of loss — wait for better signal."

    return {
        "mood": mood,
        "confidence_score": confidence,
        "plugin_signals": list(plugins.keys()),
        "forecast": forecast
    }
