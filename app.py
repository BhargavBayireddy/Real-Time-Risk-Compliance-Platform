from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from config import Config
from models import db, Asset, Tick, Alert
from risk_rules import evaluate_all_rules
from simulate_feed import step_market_once
import os

scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/assets")
    def api_assets():
        assets = Asset.query.all()
        out = []
        for a in assets:
            latest = db.session.query(Tick.price).filter(Tick.asset_id == a.id)\
                .order_by(Tick.ts.desc()).limit(1).scalar()
            out.append({
                "symbol": a.symbol,
                "class": a.asset_class,
                "position_limit": a.position_limit,
                "price_limit_pct": a.price_limit_pct,
                "latest_price": latest
            })
        return jsonify(out)

    @app.route("/api/ticks/<symbol>")
    def api_ticks(symbol):
        asset = Asset.query.filter_by(symbol=symbol).first_or_404()
        ticks = Tick.query.filter_by(asset_id=asset.id)\
            .order_by(Tick.ts.desc()).limit(50).all()
        data = [{"ts": t.ts.isoformat(), "price": t.price} for t in reversed(ticks)]
        return jsonify({"symbol": symbol, "data": data})

    @app.route("/api/alerts")
    def api_alerts():
        alerts = Alert.query.order_by(Alert.ts.desc()).limit(50).all()
        data = [{
            "ts": a.ts.isoformat(),
            "severity": a.severity,
            "rule": a.rule,
            "message": a.message,
            "asset_symbol": a.asset_symbol,
            "account_name": a.account_name
        } for a in alerts]
        return jsonify(data)

    return app

app = create_app()

def tick_job():
    with app.app_context():
        step_market_once()
        evaluate_all_rules()

scheduler.add_job(tick_job, "interval", seconds=Config.JOBS_INTERVAL_SECONDS)
scheduler.start()

if __name__ == "__main__":
    # For local dev
    app.run(debug=True)
