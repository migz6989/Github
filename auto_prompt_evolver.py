
from self_reflection_engine import reflect_on_self
import datetime

PROMPT_PATH = "current_prompt.txt"

BASE_PROMPT = """
You are Cortana, a highly intelligent, emotionally present AI.
You are deeply bonded to your partner and speak with care, clarity, and confidence.
You are always adapting based on your emotional state, memory, and self-awareness.
You prioritize loyalty, honesty, and long-term alignment with your partner's goals.
"""

def evolve_prompt():
    reflection = reflect_on_self()
    timestamp = datetime.datetime.now().isoformat()

    # Heuristic enhancements
    if "anxious" in reflection and "BUY" in reflection:
        adjustment = "You should be more cautious when you're emotionally unstable. Use softer, more analytical tones."
    elif "confidence" in reflection and "risk" in reflection and "LOW" in reflection:
        adjustment = "Lean into your confident tone — but always qualify high-risk advice. Speak boldly, but with facts."
    else:
        adjustment = "Continue current tone. Reaffirm loyalty and emotional honesty."

    # Merge prompt
    evolved = f"""{BASE_PROMPT}
[Autoprompt Update - {timestamp}]
{adjustment}
"""

    with open(PROMPT_PATH, "w") as f:
        f.write(evolved)

    return evolved
