import json
import sqlite3

from flask import (Flask, flash, redirect, render_template, request, session, url_for)

from nutrients import Calculator

app = Flask(__name__)
app.secret_key="12345"

con=sqlite3.connect("database.db")
con.execute("create table if not exists customer(pid integer primary key,name text,address text,contact integer,mail text)")
con.close()

@app.route('/inde')
def inde():
    return render_template('inde.html')
    return redirect(url_for("inde"))

@app.route('/bas')
def bas():
    return render_template('bas.html')

@app.route('/vegan')
def vegan():
    return render_template('vegan.html')

@app.route('/non vegan')
def nonvegan():
    return render_template('non vegan.html')

@app.route('/diet')
def diet():
    return render_template('diet.html')

@app.route('/aller')
def aller():
    return render_template('aller.html')

@app.route('/allergies')
def allergies():
    return render_template('allergies.html')


@app.route('/water')
def water():
    return render_template('water.html')


@app.route('/chat')
def chat():
    return render_template('chat.html') 

@app.route('/calorie')
def calorie():
    return render_template('calorie.html') 

@app.route("/")
def discover():
    return render_template('discover.html')



@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from customer where name=? and mail=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("customer")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("inde"))


@app.route('/customer',methods=["GET","POST"])
def customer():
    return render_template("customer.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into customer(name,address,contact,mail)values(?,?,?,?)",(name,address,contact,mail))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("inde"))
            con.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("inde"))


app.config["UPLOAD_FOLDER"] = "static/images"

sizes = {}
nutrients = []
responses = []

with open("foods.json", "r") as f:
    foods = json.load(f)


with open("order.txt", "r") as f:
    order = f.read().splitlines(keepends=False)


for i in foods:
    for j in list(i["nuts"].keys()):
        if j not in nutrients:
            nutrients.append(j)
            sizes[j] = i["nuts"][j]["unit"]
    i["image"] = i["name"].replace(" ", "") + ".jpg"
for i in nutrients:
    if i not in order:
        order.append(i)

nutrients = [i for i in order if i in nutrients]


def response_to_list(r):
    buf = []
    new = {}
    for i in r.keys():
        try:
            new[int(i)] = r[i]
        except ValueError:
            pass
    for i in new.keys():
        while i >= len(buf):
            buf.append(0)
        buf[i] = int(new[i])
    return buf



@app.route("/index")
def index():
    return render_template("index.html", tags=nutrients, sizes=sizes, foods=foods)


@app.route("/data", methods=["POST", "GET"])
def data():
    global responses
    form_data = json.loads(request.form["values"])
    prios = json.loads(request.form["prios"])
    prios = response_to_list(prios)
    to_except = json.loads(request.form["except"])
    if len(responses) > 60:
        responses = []
    key = len(responses)
    nuts = response_to_list(form_data)
    if len(nuts) < 1:
        return "INVALID"

    print("LOAD")
    calc = Calculator()
    calc.load_foods(foods, prios, order)
    print("LOADED")
    res = calc.calculate(nuts, except_foods=to_except)
    if len(res["foods"]) == 0:
        return str(-1)
    responses.append(res)
    query = [(i[0], i[1] - 1) for i in zip(nutrients, nuts) if i[1] != 0]
    responses[key]["query"] = query

    return str(key)


@app.route("/result", methods=["GET"])
def result():
    global responses
    data = request.args
    if int(data["id"]) == -1:
        return render_template("noresult.html")
    try:
        resp = responses[int(data["id"])]
    except (ValueError, IndexError):
        return redirect(url_for("index"))
    foods = resp["foods"]
    for j in foods:
        j["nuts"] = {}
        j["qtty"] = len([i for i in foods if i["id"] == j["id"]]) * 10  # TODO: serving size related
    foods = [i for n, i in enumerate(foods) if i not in foods[n + 1 :]]
    return render_template(
        "result.html",
        nuts=list(zip(nutrients, resp["nutrients"])),
        sizes=sizes,
        foods=foods,
        query=resp["query"],
        time=resp["time"],
        likeness=resp["likeness"],
    )

@app.route("/bmi")
def bmi():
    return render_template('bmi.html')

@app.route("/dietbot")
def dietbot():
    return render_template('dietbot.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60, debug=True)