import json


with open("foods.json", "r") as f:
    foods = json.load(f)

print("LOADED")


while 1:
    q = input("SEARCH FOOD> ").lower()
    r = [i["id"] - 2 for i in foods if q in i["name"].lower()]
    for i in r:
        print(f"[{foods[i]['id']}] {foods[i]['name']}")
    try:
        c = int(input("choice> "))
        new = foods[c - 2]
        for j in list(new["nuts"].keys()):
            print(f"{j}: {new['nuts'][j]['value']}{new['nuts'][j]['unit']}")
    except ValueError:
        pass
