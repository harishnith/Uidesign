from fyers_apiv3 import fyersModel
import pandas as pd
from datetime import datetime
from config import APP_ID, TOKEN_FILE
from db import insert_snapshot
from websocket_engine import live_prices

ACCESS_TOKEN = open(TOKEN_FILE).read().strip()

fyers = fyersModel.FyersModel(client_id=APP_ID, token=ACCESS_TOKEN)

live_data = {}

def get_chain(symbol):
    oc = fyers.optionchain({"symbol": symbol, "strikecount": 12})
    chain = oc["data"]["optionsChain"]
    return chain

def analyze(symbol):
    chain = get_chain(symbol)

    ce = [x for x in chain if x["option_type"] == "CE"]
    pe = [x for x in chain if x["option_type"] == "PE"]

    df_ce = pd.DataFrame(ce)
    df_pe = pd.DataFrame(pe)

    call_oi = df_ce["oi"].sum()
    put_oi  = df_pe["oi"].sum()

    call_vol = df_ce["volume"].sum()
    put_vol  = df_pe["volume"].sum()

    trend = "Uptrend" if put_vol > call_vol else "Downtrend"
    direction = "Bullish" if put_oi > call_oi else "Bearish"

    spot = live_prices.get(symbol, 0)

    data = {
        "symbol": symbol,
        "spot": spot,
        "call_oi": call_oi,
        "put_oi": put_oi,
        "call_vol": call_vol,
        "put_vol": put_vol,
        "trend": trend,
        "direction": direction,
        "time": datetime.now().strftime("%H:%M:%S")
    }

    insert_snapshot(data)
    return data


def update():
    global live_data

    nf = analyze("NSE:NIFTY50-INDEX")
    bn = analyze("NSE:NIFTYBANK-INDEX")

    live_data = {
        "nifty": nf,
        "bank": bn
    }