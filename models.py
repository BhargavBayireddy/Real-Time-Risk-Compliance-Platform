from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    kyc_complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Asset(db.Model):
    __tablename__ = "assets"
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False, unique=True)
    asset_class = db.Column(db.String(20), nullable=False)  # EQUITY, BOND, CRYPTO, ETF
    position_limit = db.Column(db.Integer, nullable=False, default=10000)
    price_limit_pct = db.Column(db.Float, nullable=False, default=10.0)  # % move in window

class Holding(db.Model):
    __tablename__ = "holdings"
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    account = db.relationship("Account", backref="holdings")
    asset = db.relationship("Asset", backref="holdings")

class Tick(db.Model):
    __tablename__ = "ticks"
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    ts = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    asset = db.relationship("Asset", backref="ticks")

class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    severity = db.Column(db.String(10), nullable=False)   # LOW/MED/HIGH
    rule = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    asset_symbol = db.Column(db.String(20))
    account_name = db.Column(db.String(120))
    ts = db.Column(db.DateTime, default=datetime.utcnow, index=True)

def latest_price_for(asset_id):
    return db.session.query(Tick.price).filter(Tick.asset_id == asset_id)\
        .order_by(Tick.ts.desc()).limit(1).scalar()

def price_change_pct(asset_id, window_minutes=5):
    """% change over recent window; returns None if insufficient data."""
    q = db.session.query(Tick).filter(Tick.asset_id == asset_id)\
        .order_by(Tick.ts.desc()).limit(50)
    rows = q.all()
    if len(rows) < 2:
        return None
    latest = rows[0].price
    earliest = rows[-1].price
    if earliest == 0:
        return None
    return (latest - earliest) / earliest * 100.0
