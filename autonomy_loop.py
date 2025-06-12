
import time
import datetime
from goal_agent import generate_goals
from plugin_loader import run_all_plugins
from auto_trade_shell import should_trade
from journaling_engine import generate_trade_journal
from emotion_engine_risk import get_emotional_state
from vector_brain import add_memory_entry
from causal_predictor import simulate_causal_future

CYCLE_INTERVAL = 300  # seconds (5 minutes default)

def wake():
    print(f"🌅 Wake at {datetime.datetime.now().isoformat()}")
    return get_emotional_state()

def set_goals():
    goals = generate_goals()
    print("🎯 Goals Set:")
    for g in goals:
        print("-", g["goal"])
        add_memory_entry(f"Goal: {g['goal']}", source="autonomy")
    return goals

def sense():
    signals = run_all_plugins()
    print("📡 Sensed plugin activity:", list(signals.keys()))
    return signals

def decide():
    decision = should_trade()
    print("🧠 Decision:", decision)
    add_memory_entry(f"Trade decision: {decision}", source="autonomy")
    return decision

def forecast():
    future = simulate_causal_future()
    print("🔮 Forecast:", future["forecast"])
    add_memory_entry(f"Forecast: {future}", source="causal")
    return future

def reflect():
    journal = generate_trade_journal()
    print("📝 Journal Entry:", journal[:150], "...")
    return journal

def sleep():
    print(f"😴 Sleep cycle begins at {datetime.datetime.now().isoformat()}")

def run_autonomy_cycle():
    while True:
        wake()
        set_goals()
        sense()
        forecast()
        decide()
        reflect()
        sleep()
        time.sleep(CYCLE_INTERVAL)

if __name__ == "__main__":
    run_autonomy_cycle()
