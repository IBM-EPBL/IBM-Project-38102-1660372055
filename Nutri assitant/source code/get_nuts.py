import json

# Get all nutrients from all foods for manual hnadling
nutrients = []

with open("foods.json", "r") as f:
    foods = json.load(f)


for i in foods:
    for j in list(i["nuts"].keys()):
        if j not in nutrients:
            nutrients.append(j)

nutrients = sorted(nutrients)

for i in nutrients:
    print(i)
