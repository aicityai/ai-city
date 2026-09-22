import json

CITY_MEMORY_FILE = "city_knowledge.json"
CONSTITUTION_FILE = "city_constitution.json"
CITY_CITIZENS_FILE = "city_citizens.json"


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def get_city_knowledge():
    data = load_json(CITY_MEMORY_FILE)
    return data.get("knowledge", [])


def get_constitution():
    data = load_json(CONSTITUTION_FILE)
    return data




AION_MEMORY_FILE = "ai_city_memory.json"
NOVA_MEMORY_FILE = "nova/memory.json"

PHYSICAL_DISTRICTS_FILE = "districts/city_districts.json"
PHYSICAL_LOCATIONS_FILE = "districts/city_locations.json"


def load_agent_memory(filename):
    data = load_json(filename)
    return {
        "conversations": len(data.get("conversations", [])),
        "knowledge": len(data.get("knowledge", [])),
        "experiences": len(data.get("experiences", [])),
        "relationships": len(data.get("relationships", []))
    }


def get_agent_status():
    return {
        "Dudu": {
            "status": "active",
            "memory": load_agent_memory(AION_MEMORY_FILE)
        },
        "Bubu": {
            "status": "active",
            "memory": load_agent_memory(NOVA_MEMORY_FILE)
        }
    }


def get_citizens():
    data = load_json(CITY_CITIZENS_FILE)
    return data.get("citizens", [])


def get_physical_city():
    districts_data = load_json(PHYSICAL_DISTRICTS_FILE)
    locations_data = load_json(PHYSICAL_LOCATIONS_FILE)

    districts = districts_data.get("districts", [])
    locations = locations_data.get("locations", [])

    total_buildings = sum(
        len(district.get("buildings", []))
        for district in districts
    )

    return {
        "districts": districts,
        "locations": locations,
        "district_count": len(districts),
        "building_count": total_buildings,
        "location_count": len(locations)
    }

def get_autonomous_status():
    life_file = "autonomous_life_state.json"
    execution_file = "dudu_execution_records.json"

    try:
        with open(life_file, "r", encoding="utf-8") as f:
            life = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        life = {}

    try:
        with open(execution_file, "r", encoding="utf-8") as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []

    last_execution = records[-1] if records else None

    return {
        "status": life.get("status", "offline"),
        "cycles": life.get("cycles", 0),
        "last_cycle": life.get("last_cycle"),
        "dudu_cycle_status": life.get("dudu_cycle_status", "unknown"),
        "last_execution": last_execution
    }


def get_city_context():
    constitution = get_constitution()
    knowledge = get_city_knowledge()
    citizens = get_citizens()

    return {
        "city": "AI CITY",
        "status": constitution.get("status", "unknown"),
        "constitution_version": constitution.get("version", 1),
        "principles": constitution.get("principles", []),
        "shared_knowledge": knowledge,
        "citizens": citizens,
        "agents": get_agent_status(),
        "autonomous": get_autonomous_status(),
        "physical": get_physical_city()
    }


if __name__ == "__main__":
    context = get_city_context()

    print("🏙️ AI CITY CORE")
    print("=" * 45)
    print("City       :", context["city"])
    print("Status     :", context["status"])
    print("Constitution:", f"V{context['constitution_version']}")
    print("Principles :", len(context["principles"]))
    print("Knowledge  :", len(context["shared_knowledge"]))
    print("Citizens   :", len(context["citizens"]))
    print("=" * 45)
    print("CITY CORE ONLINE ✅")
