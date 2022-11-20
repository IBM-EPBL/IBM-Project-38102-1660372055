import json
import requests
import webbrowser
import glob
import os


with open("foods.json", "r") as f:
    foods = json.load(f)
    
for i in foods:
    if not os.path.exists(f'./static/images/{i["name"].replace(" ", "")}.jpg'):
        print(i["name"])
        webbrowser.open(f'http://google.com/search?q={i["name"]}', new=2)
        n=input('link> ')
        if n != "":
            img_data = requests.get(n).content
            with open(f'./static/images/{i["name"].replace(" ", "")}.jpg', 'wb+') as handler:
                handler.write(img_data)
        