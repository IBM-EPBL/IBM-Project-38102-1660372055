import json


AVG = [
    (
        "Omega 3",
        (
            "PUFA 18:3",
            "PUFA 18:4",
            "PUFA 20:4",
            "PUFA 20:5 n-3 (EPA)",
            "PUFA 22:5 n-3 (DPA)",
            "PUFA 22:6 n-3 (DHA)",
        ),
    ),
]

with open("foods.json", "r") as f:
    foods = json.load(f)

for food in foods:
    for (group, contents) in AVG:
        food["nuts"][group] = {"value": 0, "unit": ""}
        found = 0
        for nut in food["nuts"]:
            if nut in contents:
                food["nuts"][group]["unit"] = food["nuts"][nut]["unit"]
                food["nuts"][group]["value"] += food["nuts"][nut]["value"]
                found += 1
        if found > 0:
            food["nuts"][group]["value"] = round(food["nuts"][group]["value"], 2)

with open("foods.json", "w") as f:
    json.dump(foods, f)
