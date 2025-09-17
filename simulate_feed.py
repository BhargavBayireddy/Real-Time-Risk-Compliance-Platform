import random
from datetime import datetime
import yfinance as yf
from models import db, Asset, Tick

def step_market_once():
    assets = Asset.query.all()
    for a in assets:
        symbol = a.symbol
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.history(period="1m", interval="1m")["Close"].iloc[-1]
            db.session.add(Tick(asset_id=a.id, price=round(float(price), 2)))
        except Exception as e:
            print(f"Failed to fetch {symbol}, using fallback. Error: {e}")
            db.session.add(Tick(asset_id=a.id, price=100.0))
    db.session.commit()


def seed_initial_ticks():
    assets = Asset.query.all()
    for a in assets:
        base = random.uniform(50, 250)
        t = Tick(asset_id=a.id, price=round(base, 2))
        db.session.add(t)
    db.session.commit()