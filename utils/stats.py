import json
import os

STATS_FILE = "stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"users": [], "files": 0, "storage": 0}
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def save_stats(data):
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(user_id):
    stats = load_stats()
    if user_id not in stats["users"]:
        stats["users"].append(user_id)
        save_stats(stats)

def add_file(file_size):
    stats = load_stats()
    stats["files"] += 1
    stats["storage"] += file_size
    save_stats(stats)

def get_stats():
    stats = load_stats()
    return stats
