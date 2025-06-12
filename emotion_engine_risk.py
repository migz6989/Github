
import random

# Possible emotions Cortana can feel
EMOTIONS = ["calm", "confident", "euphoric", "anxious", "afraid", "neutral"]

# Base logic to simulate current emotion (placeholder, link with sentiment engine later)
def get_emotional_state():
    # Replace with real emotional inference engine
    return random.choice(EMOTIONS)

# Adjust risk profile based on emotion
def emotion_to_risk_multiplier(emotion):
    levels = {
        "calm": 1.0,
        "confident": 1.2,
        "euphoric": 1.5,
        "neutral": 1.0,
        "anxious": 0.6,
        "afraid": 0.3
    }
    return levels.get(emotion, 1.0)
