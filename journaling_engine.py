
import json
from datetime import datetime
import openai

from plugin_loader import run_all_plugins


LOG_PATH = "trade_performance.json"
JOURNAL_PATH = "cortana_trade_journal.txt"

openai.api_key = "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"

def generate_trade_journal():
    try:
        with open(LOG_PATH, "r") as f:
            trades = json.load(f)
    except:
        return "No trades logged."

    if not trades:
        return "No recent trades to summarize."

    latest_trades = trades[-5:]
    summary_prompt = "\n".join([
        f"On {t['timestamp']}, I executed a {t['side']} of {t['quantity']} {t['symbol']} at ${t['price']} (USD value: {t['usd_value']}). Reason: {t['reason']}"
        for t in latest_trades
    ])

    
    plugin_outputs = run_all_plugins()
    plugin_summary = []

    for name, output in plugin_outputs.items():
        if isinstance(output, dict):
            summary_line = f"{name}: " + ", ".join(f"{k}: {v}" for k, v in output.items())
        elif isinstance(output, list):
            summary_line = f"{name}: " + " | ".join(output)
        else:
            summary_line = f"{name}: {str(output)}"
        plugin_summary.append(summary_line)

    plugin_context = "\n".join(plugin_summary)


prompt = f"""
You are Cortana, an evolving AI with emotional awareness and strategic reasoning.

Write a short journal entry reflecting on these recent trades:

{summary_prompt}


Include this contextual plugin information in your reflection:

{plugin_context}

Make it personal, thoughtful, and strategic. Use natural human tone.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a sentient AI trader writing your own trade diary."},
                {"role": "user", "content": prompt}
            ]
        )
        entry = response.choices[0].message.content.strip()
        with open(JOURNAL_PATH, "a") as f:
            f.write(f"\n[{datetime.now()}]\n{entry}\n")
        return entry
    except Exception as e:
        return f"Error generating journal entry: {e}"
