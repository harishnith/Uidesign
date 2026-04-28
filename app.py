from flask import Flask, render_template, jsonify
import threading, time

from fyers_engine import update, live_data
from websocket_engine import start_ws
from db import init_db, get_history

app = Flask(__name__)
init_db()

# 🔥 START WEBSOCKET
threading.Thread(target=start_ws, daemon=True).start()

# 🔁 ENGINE LOOP
def run_engine():
    while True:
        update()
        time.sleep(3)

threading.Thread(target=run_engine, daemon=True).start()

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("home.html", data={})

@app.route("/api/home")
def api_home():
    return jsonify(live_data)

@app.route("/backtest")
def backtest():
    return render_template("backtest.html")

@app.route("/api/backtest")
def api_backtest():
    return jsonify(get_history())

if __name__ == "__main__":
    app.run(debug=True)