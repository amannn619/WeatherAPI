from flask import Flask, render_template
import pandas as pd

app =Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]][:92]
@app.route("/")
def home():
    return render_template("home.html", data= stations.to_html())

@app.route("/api/<station>/<date>")
def api(station, date):
    fileno = "00000"+station
    if len(fileno) > 6:
        fileno = fileno[len(fileno) - 6:]
    try:
        df = pd.read_csv(f"data_small/TG_STAID{fileno}.txt", skiprows=20, parse_dates=["    DATE"])
        temp = df.loc[df["    DATE"] == date]["   TG"].squeeze()
    except FileNotFoundError:
        return {"Error": "The Station Code is Invalid"}

    return {"station": station,
            "date": date,
            "temperature": str(temp)}

@app.route("/api/<station>")
def station(station):
    fileno = "00000"+station
    if len(fileno) > 6:
        fileno = fileno[len(fileno) - 6:]
    try:
        df = pd.read_csv(f"data_small/TG_STAID{fileno}.txt", skiprows=20, parse_dates=["    DATE"])
        res = {}
        df = df[["    DATE", "   TG"]].to_dict()
        for i,j in zip(df["    DATE"].values() , df["   TG"].values()) :
            res[str(i.date())] = j/10
        
    except FileNotFoundError:
        return {"Error": "The Station Code is Invalid"}
    
    return res
    
@app.route("/api/yearly/<station>/<year>")
def yearly(station, year):
    if len(year)>4:
        return {"Error": "Year not valid!"}
    fileno = "00000"+station
    if len(fileno) > 6:
        fileno = fileno[len(fileno) - 6:]
        print(fileno)
    try:
        df = pd.read_csv(f"data_small/TG_STAID{fileno}.txt", skiprows=20, parse_dates=["    DATE"])
        data = df.loc[df["    DATE"].dt.year == int(year)]
        data = data.to_dict()
        res = {}
        for i, j in zip(data["    DATE"].values(), data["   TG"].values()):
            res[str(i.date())] = j/10

    except FileNotFoundError :
        return {"Error": "The Station Code is Invalid"}
    
    return res

if __name__ == "__main__":
    app.run()