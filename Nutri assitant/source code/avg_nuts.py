import json


# Get the average and put it in a new nutrient
AVG = [
    ("Carbohydrates", ("Carbohydrate, by difference", "Carbohydrate, by summation")),
    ("Calories", ("Energy (Atwater General Factors)", "Energy (Atwater Specific Factors)")),
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
            food["nuts"][group]["value"] = round(food["nuts"][group]["value"] / found, 2)

with open("foods.json", "w") as f:
    json.dump(foods, f)
