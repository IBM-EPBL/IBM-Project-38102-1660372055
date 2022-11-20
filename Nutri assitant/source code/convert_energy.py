import json


with open("foods.json", "r") as f:
    foods = json.load(f)

for food in foods:
    energy = food["nuts"]["Energy"]
    if "kj" in energy["unit"].lower():
        print("a")
        energy["value"] *= 0.24
        energy["unit"] = "kcal"

with open("foods.json", "w") as f:
    json.dump(foods, f)
