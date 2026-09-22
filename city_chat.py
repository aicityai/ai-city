import json
from datetime import datetime

CHAT_FILE = "city_chat.json"
def load_chat():
    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"messages": []}

def send_message(sender, receiver, message):
    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        chat = json.load(f)

    chat.setdefault("messages", []).append({
        "timestamp": datetime.now().isoformat(),
        "sender": sender,
        "receiver": receiver,
        "message": message
    })

    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat, f, ensure_ascii=False, indent=2)


def get_messages(receiver):
    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        chat = json.load(f)

    return [
        m for m in chat.get("messages", [])
        if m["receiver"] == receiver
    ]

def load_city_knowledge():
    with open("city_knowledge.json", "r", encoding="utf-8") as f:
        return json.load(f)


def add_city_knowledge(source, knowledge):
    data = load_city_knowledge()

    entry = {
        "source": source,
        "knowledge": knowledge,
        "timestamp": datetime.now().isoformat()
    }

    data.setdefault("knowledge", []).append(entry)

    with open("city_knowledge.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_city_knowledge():
    data = load_city_knowledge()
    return data.get("knowledge", [])
