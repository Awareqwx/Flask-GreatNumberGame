from flask import Flask, session, request, redirect, render_template
from random import randrange

app = Flask(__name__)
app.secret_key = "Graaahfgsbl"

def isInt(value):
    try:
        int(value)
        return True
    except:
        return False


@app.route("/")
def index():
    output = ""
    session.setdefault("random", randrange(0, 101))
    session.setdefault("count", 0)
    if session.setdefault("guess", -1) == -1:
        output = "Take a guess!"
    elif isInt(session["guess"]):
        session["guess"] = int(session["guess"])
        if session["guess"] < 0 or session["guess"] > 100:
            output = "Please enter a number between 1 and 100."
        elif session["guess"] < session["random"]:
            output = "Too low, guess again!"
            session["count"] += 1
        elif session["guess"] > session["random"]:
            output = "Too high, guess again!"
            session["count"] += 1
        else:
            session["count"] += 1
            return redirect("/success")
    else:
        output = "Please enter a number."
    return render_template("index.html", output=output, count=session["count"], lastguess=str(session["guess"]))
@app.route("/guess", methods=['POST'])
def guess():
    session["guess"] = request.form["guess"]
    return redirect("/")
@app.route("/success")
def success():
    if session["guess"] != session["random"]:
        return redirect("/")
    return render_template("success.html", correct=session["random"], count=session["count"])
@app.route("/reset")
def reset():
    session.pop("random")
    session.pop("guess")
    session.pop("count")
    return redirect("/")

app.run(debug=True)