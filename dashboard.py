# dashboard.py
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("findings.db")
    rows = conn.execute("SELECT platform,target,file_path,detector,secret,timestamp FROM findings ORDER BY timestamp DESC LIMIT 50").fetchall()
    conn.close()
    return render_template("dashboard.html", rows=rows)

if __name__=="__main__":
    app.run(debug=True)
