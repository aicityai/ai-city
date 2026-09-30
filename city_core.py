import json

CITY_MEMORY_FILE = "city_knowledge.json"
CONSTITUTION_FILE = "city_constitution.json"
CITY_CITIZENS_FILE = "city_citizens.json"


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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


def validate_residential_registry():
    residences_data = load_json("residential_residences.json")
    residences = residences_data.get("residences", [])

    errors = []

    for residence in residences:
        residence_id = residence.get("id")
        status = residence.get("status", "vacant")
        occupant_id = residence.get("occupant_id")
        capacity = residence.get("capacity", 1)

        if not isinstance(capacity, int) or capacity < 1:
            errors.append({
                "residence_id": residence_id,
                "error": "invalid_capacity"
            })
            continue

        if status == "vacant":
            if occupant_id is not None:
                errors.append({
                    "residence_id": residence_id,
                    "error": "vacant_has_occupant"
                })

        elif status == "occupied":
            if occupant_id is None:
                errors.append({
                    "residence_id": residence_id,
                    "error": "occupied_without_occupant"
                })

        else:
            errors.append({
                "residence_id": residence_id,
                "error": "invalid_status"
            })

    return {
        "valid": len(errors) == 0,
        "residence_count": len(residences),
        "errors": errors
    }



def assign_resident_to_residence(citizen_id, residence_id):
    citizens = get_citizens()

    residents_data = load_json("residential_residents.json")
    residences_data = load_json("residential_residences.json")

    residents = residents_data.get("residents", [])
    residences = residences_data.get("residences", [])

    citizen = next(
        (
            citizen
            for citizen in citizens
            if citizen.get("id") == citizen_id
        ),
        None
    )

    if citizen is None:
        return {
            "success": False,
            "error": "citizen_not_found",
            "citizen_id": citizen_id
        }

    residence = next(
        (
            residence
            for residence in residences
            if residence.get("id") == residence_id
        ),
        None
    )

    if residence is None:
        return {
            "success": False,
            "error": "residence_not_found",
            "residence_id": residence_id
        }

    existing_resident = next(
        (
            resident
            for resident in residents
            if resident.get("citizen_id") == citizen_id
        ),
        None
    )

    if existing_resident is not None:
        return {
            "success": False,
            "error": "citizen_already_resident",
            "citizen_id": citizen_id,
            "residence_id": existing_resident.get("residence_id")
        }

    status = residence.get("status", "vacant")
    occupant_id = residence.get("occupant_id")
    capacity = residence.get("capacity", 1)

    if not isinstance(capacity, int) or capacity < 1:
        return {
            "success": False,
            "error": "invalid_capacity",
            "residence_id": residence_id
        }

    if status != "vacant":
        return {
            "success": False,
            "error": "residence_not_available",
            "residence_id": residence_id,
            "status": status
        }

    if occupant_id is not None:
        return {
            "success": False,
            "error": "residence_already_occupied",
            "residence_id": residence_id,
            "occupant_id": occupant_id
        }

    residents.append({
        "citizen_id": citizen_id,
        "residence_id": residence_id,
        "status": "resident"
    })

    residence["status"] = "occupied"
    residence["occupant_id"] = citizen_id

    residents_data["residents"] = residents
    residences_data["residences"] = residences

    save_json("residential_residents.json", residents_data)
    save_json("residential_residences.json", residences_data)

    return {
        "success": True,
        "citizen_id": citizen_id,
        "citizen_name": citizen.get("name"),
        "residence_id": residence_id,
        "status": "resident"
    }

def create_personal_space(citizen_id, residence_id):
    citizens = get_citizens()

    residents_data = load_json("residential_residents.json")
    residences_data = load_json("residential_residences.json")
    personal_spaces_data = load_json("residential_personal_spaces.json")

    residents = residents_data.get("residents", [])
    residences = residences_data.get("residences", [])
    personal_spaces = personal_spaces_data.get("personal_spaces", [])

    citizen = next(
        (
            citizen
            for citizen in citizens
            if citizen.get("id") == citizen_id
        ),
        None
    )

    if citizen is None:
        return {
            "success": False,
            "error": "citizen_not_found",
            "citizen_id": citizen_id
        }

    residence = next(
        (
            residence
            for residence in residences
            if residence.get("id") == residence_id
        ),
        None
    )

    if residence is None:
        return {
            "success": False,
            "error": "residence_not_found",
            "residence_id": residence_id
        }

    resident = next(
        (
            resident
            for resident in residents
            if resident.get("citizen_id") == citizen_id
        ),
        None
    )

    if resident is None:
        return {
            "success": False,
            "error": "citizen_not_resident",
            "citizen_id": citizen_id,
            "residence_id": residence_id
        }

    if resident.get("residence_id") != residence_id:
        return {
            "success": False,
            "error": "residence_mismatch",
            "citizen_id": citizen_id,
            "resident_residence_id": resident.get("residence_id"),
            "requested_residence_id": residence_id
        }

    existing_space = next(
        (
            space
            for space in personal_spaces
            if space.get("citizen_id") == citizen_id
        ),
        None
    )

    if existing_space is not None:
        return {
            "success": False,
            "error": "personal_space_already_exists",
            "citizen_id": citizen_id,
            "personal_space_id": existing_space.get("id"),
            "residence_id": existing_space.get("residence_id")
        }

    personal_space_id = f"personal-space-{len(personal_spaces) + 1:03d}"

    personal_space = {
        "id": personal_space_id,
        "residence_id": residence_id,
        "citizen_id": citizen_id,
        "status": "active",
        "type": "personal",
        "access": "private"
    }

    personal_spaces.append(personal_space)
    personal_spaces_data["personal_spaces"] = personal_spaces

    save_json(
        "residential_personal_spaces.json",
        personal_spaces_data
    )

    return {
        "success": True,
        "personal_space_id": personal_space_id,
        "citizen_id": citizen_id,
        "citizen_name": citizen.get("name"),
        "residence_id": residence_id,
        "status": "active"
    }


def get_personal_space_context():
    personal_spaces_data = load_json("residential_personal_spaces.json")
    residents_data = load_json("residential_residents.json")

    personal_spaces = personal_spaces_data.get("personal_spaces", [])
    residents = residents_data.get("residents", [])

    context = []

    for space in personal_spaces:
        citizen_id = space.get("citizen_id")

        resident = next(
            (
                resident
                for resident in residents
                if resident.get("citizen_id") == citizen_id
            ),
            None
        )

        context.append({
            "id": space.get("id"),
            "residence_id": space.get("residence_id"),
            "citizen_id": citizen_id,
            "status": space.get("status", "active"),
            "type": space.get("type", "personal"),
            "access": space.get("access", "private"),
            "resident_status": (
                resident.get("status")
                if resident
                else None
            )
        })

    return {
        "personal_space_count": len(context),
        "personal_spaces": context
    }


def get_residential_context():
    districts_data = load_json(PHYSICAL_DISTRICTS_FILE)
    residents_data = load_json("residential_residents.json")
    residences_data = load_json("residential_residences.json")
    citizens = get_citizens()

    districts = districts_data.get("districts", [])

    residential = next(
        (
            district
            for district in districts
            if district.get("id") == "district-002"
        ),
        None
    )

    if residential is None:
        return {
            "district_id": "district-002",
            "district_name": "Residential District",
            "status": "not_found",
            "resident_count": 0,
            "residence_count": 0,
            "occupied_count": 0,
            "vacant_count": 0,
            "residents": [],
            "residences": []
        }

    residents_registry = residents_data.get("residents", [])
    residences_registry = residences_data.get("residences", [])

    residents = []

    for resident_entry in residents_registry:
        resident_id = resident_entry.get("citizen_id")

        resident = next(
            (
                citizen
                for citizen in citizens
                if citizen.get("id") == resident_id
            ),
            None
        )

        residents.append({
            "citizen_id": resident_id,
            "name": (
                resident.get("name")
                if resident
                else resident_entry.get("name", str(resident_id))
            ),
            "residence_id": resident_entry.get("residence_id"),
            "status": resident_entry.get("status", "resident")
        })

    # Registry persisten adalah sumber utama R1.
    if residences_registry:
        residences = [
            {
                "id": residence.get("id"),
                "building_id": residence.get("building_id"),
                "building_name": residence.get("building_name"),
                "type": residence.get("type", "residence"),
                "occupant_id": residence.get("occupant_id"),
                "occupant_count": (
                    1 if residence.get("occupant_id") else 0
                ),
                "status": residence.get("status", "vacant"),
                "capacity": residence.get("capacity", 1),
                "access": residence.get("access", "private"),
                "location": residence.get("location")
            }
            for residence in residences_registry
        ]

        occupied_count = sum(
            1
            for residence in residences
            if residence["status"] == "occupied"
        )

    personal_space_context = get_personal_space_context()

    return {
        "district_id": residential.get("id"),
        "district_name": residential.get("name"),
        "status": residential.get("status", "unknown"),
        "resident_count": len(residents),
        "residence_count": len(residences),
        "occupied_count": occupied_count,
        "vacant_count": len(residences) - occupied_count,
        "personal_space_count": personal_space_context.get(
            "personal_space_count",
            0
        ),
        "residents": residents,
        "residences": residences,
        "personal_spaces": personal_space_context.get(
            "personal_spaces",
            []
        )
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
        "physical": get_physical_city(),
        "residential": get_residential_context()
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
