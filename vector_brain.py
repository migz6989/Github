
import os
import json
from datetime import datetime

MEMORY_FILE = "cortana_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

def add_memory_entry(text, source="system"):
    mem = load_memory()
    entry = {
        "text": text,
        "source": source,
        "timestamp": datetime.now().isoformat()
    }
    mem.append(entry)
    save_memory(mem)
    return entry

def query_memory(keyword):
    mem = load_memory()
    return [m["text"] for m in mem if keyword.lower() in m["text"].lower()]
