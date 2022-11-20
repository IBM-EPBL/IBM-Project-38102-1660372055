import json


with open("foods.json", "r") as f:
    foods = json.load(f)

print("LOADED")

todel = []

print(len(foods))
for i in foods:
    inp = input(f"set limit for {i['name']} )({i['limit']})> ")
    if inp == "q":
        break
    elif inp == "d":
        todel.append(foods.index(i))
    try:
        inp = int(inp)
        i['limit'] = inp
    except ValueError:
        pass

for i in todel:
    del foods[i]

with open("foods.json", "w") as f:
    json.dump(foods, f)
