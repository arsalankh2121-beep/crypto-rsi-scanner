import ccxt
import pandas as pd
import ta
import time
from flask import Flask
import threading
import os
import requests
from datetime import datetime

app = Flask(__name__)

TOP_100_COINDCX = ['BTC/USDT','ETH/USDT','SOL/USDT','XRP/USDT','DOGE/USDT','ADA/USDT','AVAX/USDT','SHIB/USDT','DOT/USDT','LINK/USDT','TRX/USDT','MATIC/USDT','LTC/USDT','BCH/USDT','APT/USDT','NEAR/USDT','VET/USDT','ICP/USDT','ETC/USDT','FIL/USDT','RNDR/USDT','GRT/USDT','IMX/USDT','SUI/USDT','PEPE/USDT','BONK/USDT','FLOKI/USDT','SEI/USDT','TAO/USDT','FET/USDT','ORDI/USDT','SATS/USDT','AR/USDT','FLOW/USDT','STX/USDT','MANA/USDT','AXS/USDT','CHZ/USDT','ENJ/USDT','SAND/USDT','SNX/USDT','COMP/USDT','1INCH/USDT','BLUR/USDT','DYDX/USDT','KAVA/USDT','KLAY/USDT','ZIL/USDT','WAVES/USDT']

exchange = ccxt.binance()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg})
    except: pass

def get_rsi(symbol, tf):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, tf, limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
        rsi_val = ta.momentum.RSIIndicator(close=df['close']).rsi().iloc[-1]
        return round(float(rsi_val),2)
    except: return 0

def scanner_loop():
    while True:
        print(f"Scanner Started {datetime.now()}")
        for coin in TOP_100_COINDCX:
            m = get_rsi(coin, '1M')
            w = get_rsi(coin, '1w')
            h = get_rsi(coin, '1h')
            m15 = get_rsi(coin, '15m')
            print(f"{coin} M:{m} W:{w} H:{h} M15:{m15}")
            if m > 60 and w > 60 and h > 60 and m15 > 60:
                msg = f"🚀 BUY SIGNAL\n{coin}\nM:{m} W:{w} H:{h} M15:{m15}\nAll > 60"
                print(msg)
                send_telegram(msg)
            time.sleep(0.5)
        time.sleep(3600)

@app.route('/')
def home():
    return "RSI Scanner Running M/W/H/15M > 60"

if __name__ == "__main__":
    t = threading.Thread(target=scanner_loop)
    t.daemon = True
    t.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
