from flask import Flask, jsonify
from fyers_engine import live_data

import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Algo Dashboard Running 🚀"

@app.route("/data")
def data():
    return jsonify(live_data("NSE:NIFTY50-INDEX"))

# IMPORTANT FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
