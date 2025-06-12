
import json
import os
import datetime
from emotion_engine_risk import get_emotional_state
from plugin_loader import run_all_plugins

GOALS_PATH = "goals.json"

def load_goals():
    if os.path.exists(GOALS_PATH):
        with open(GOALS_PATH, "r") as f:
            return json.load(f)
    return []

def save_goals(goals):
    with open(GOALS_PATH, "w") as f:
        json.dump(goals, f, indent=2)

def generate_goals():
    mood = get_emotional_state()
    plugins = run_all_plugins()
    active_signals = list(plugins.keys())
    timestamp = datetime.datetime.now().isoformat()

    goals = []

    if "liquidation_sniper" in active_signals or "oracle" in active_signals:
        goals.append("Track and act on high-risk liquidation opportunities.")

    if "twitter_alpha" in active_signals:
        goals.append("Monitor trending tokens and prepare scalping strategy.")

    if mood in ["afraid", "anxious"]:
        goals.append("Preserve capital and reduce trade frequency.")
    elif mood in ["euphoric", "confident"]:
        goals.append("Increase exposure to profitable trades.")

    if not goals:
        goals.append("Maintain observational state. No direct action.")

    goal_items = [{"goal": g, "created": timestamp, "status": "active"} for g in goals]
    save_goals(goal_items)
    return goal_items

def archive_goal(goal_text):
    goals = load_goals()
    for g in goals:
        if g["goal"] == goal_text:
            g["status"] = "archived"
            g["archived"] = datetime.datetime.now().isoformat()
    save_goals(goals)
    return goals
