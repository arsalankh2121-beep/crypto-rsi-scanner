import ccxt
import pandas as pd
import ta
import time
from flask import Flask
import threading
import os
from datetime import datetime

app = Flask(__name__)

# CoinDCX Top 100 - Final List
TOP_100_COINDCX = [
    'BTC/USDT','ETH/USDT','SOL/USDT','XRP/USDT','BNB/USDT','DOGE/USDT','ADA/USDT','AVAX/USDT','SHIB/USDT','DOT/USDT',
    'LINK/USDT','TRX/USDT','MATIC/USDT','LTC/USDT','BCH/USDT','UNI/USDT','XLM/USDT','ETC/USDT','FIL/USDT','HBAR/USDT',
    'APT/USDT','NEAR/USDT','VET/USDT','ICP/USDT','ATOM/USDT','ARB/USDT','MKR/USDT','OP/USDT','STX/USDT','INJ/USDT',
    'RNDR/USDT','GRT/USDT','IMX/USDT','SUI/USDT','AAVE/USDT','PEPE/USDT','FET/USDT','TAO/USDT','RUNE/USDT','WIF/USDT',
    'BONK/USDT','FLOKI/USDT','SEI/USDT','JUP/USDT','ONDO/USDT','ENA/USDT','W/USDT','PYTH/USDT','STRK/USDT','TIA/USDT',
    'ORDI/USDT','SATS/USDT','AR/USDT','FLOW/USDT','EGLD/USDT','XTZ/USDT','THETA/USDT','SAND/USDT',
    'MANA/USDT','AXS/USDT','CHZ/USDT','ENJ/USDT','GALA/USDT','APE/USDT','LDO/USDT','RPL/USDT','FXS/USDT','CRV/USDT',
    'SNX/USDT','COMP/USDT','1INCH/USDT','ENS/USDT','BAT/USDT','ZRX/USDT','QTUM/USDT','IOTA/USDT','NEO/USDT','EOS/USDT',
    'KAVA/USDT','KLAY/USDT','ZIL/USDT','WAVES/USDT','CELO/USDT','ONE/USDT','ALGO/USDT','XAUT/USDT','PAXG/USDT'
]

exchange = ccxt.binance()

def get_rsi(symbol, tf):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, tf, limit=200)
        df = pd.DataFrame(ohlcv, columns=['t','o','h','l','c','v'])
        rsi = ta.momentum.RSIIndicator(close=df['c'], window=14).rsi().iloc[-1]
        return round(rsi,2)
    except:
        return 0

def scanner_loop():
    while True:
        print(f"\n--- Scanner Started at {datetime.now()} ---\n")
        for coin in TOP_100_COINDCX:
            m = get_rsi(coin, '1M')
            w = get_rsi(coin, '1w')
            h = get_rsi(coin, '1h')
            m15 = get_rsi(coin, '15m')
            
            if m > 60 and w > 60 and h > 60 and m15 > 60:
                print(f"🚀 BUY: {coin} | M:{m} W:{w} H:{h} 15m:{m15}")
            time.sleep(0.5)
        print("--- Scan Complete, sleeping 1 hour ---")
        time.sleep(3600)

@app.route('/')
def home():
    return "Crypto RSI Scanner is Running!"

if __name__ == "__main__":
    t = threading.Thread(target=scanner_loop)
    t.daemon = True
    t.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
