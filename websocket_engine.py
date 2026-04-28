from fyers_apiv3.FyersWebsocket import data_ws
from config import APP_ID, TOKEN_FILE, SYMBOLS

ACCESS_TOKEN = open(TOKEN_FILE).read().strip()

live_prices = {}

def onmessage(msg):
    try:
        if "symbol" in msg:
            live_prices[msg["symbol"]] = msg.get("ltp", 0)
    except:
        pass

def onopen():
    ws.subscribe(symbols=SYMBOLS, data_type="symbolData")
    ws.keep_running()

def start_ws():
    global ws
    ws = data_ws.FyersDataSocket(
        access_token=ACCESS_TOKEN,
        log_path="",
        litemode=True,
        write_to_file=False,
        reconnect=True,
        on_connect=onopen,
        on_message=onmessage
    )
    ws.connect()