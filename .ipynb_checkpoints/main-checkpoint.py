from flask import Flask, render_template

app =Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/<station>/<date>")
def api(station, date):
    temp = 10
    return {"station": station,
            "date": date,
            "temperature": temp}

if __name__ == "__main__":
    app.run(debug=True)