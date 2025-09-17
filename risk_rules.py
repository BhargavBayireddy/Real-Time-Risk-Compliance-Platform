from models import db, Asset, Holding, Account, Alert, price_change_pct, latest_price_for

def raise_alert(severity, rule, message, asset_symbol=None, account_name=None):
    alert = Alert(severity=severity, rule=rule, message=message,
                  asset_symbol=asset_symbol, account_name=account_name)
    db.session.add(alert)

def rule_position_limit():
    """Alert when any holding exceeds the asset's position limit."""
    holdings = db.session.query(Holding).all()
    for h in holdings:
        limit = h.asset.position_limit
        if h.quantity > limit:
            raise_alert(
                "HIGH",
                "POSITION_LIMIT",
                f"⚠️ Too many shares of {h.asset.symbol}! You hold {h.quantity}, but the safe limit is {limit}.",
                asset_symbol=h.asset.symbol,
                account_name=h.account.name
            )

def rule_price_spike():
    """Alert when price move > asset.price_limit_pct over window."""
    assets = db.session.query(Asset).all()
    for a in assets:
        pct = price_change_pct(a.id, window_minutes=5)
        if pct is None:
            continue
        if abs(pct) >= a.price_limit_pct:
            raise_alert(
                "HIGH",
                "PRICE_SPIKE",
                f"📈 Big price movement in {a.symbol}! Changed {pct:.2f}% which is above the allowed {a.price_limit_pct:.2f}%.",
                asset_symbol=a.symbol
            )

def rule_trade_halts_on_missing_kyc():
    """If account KYC is missing but they hold > 0 quantity, flag."""
    holdings = db.session.query(Holding).all()
    for h in holdings:
        if not h.account.kyc_complete and h.quantity > 0:
            raise_alert(
                "MED",
                "KYC_MISSING",
                f"Account '{h.account.name}' holds {h.quantity} of {h.asset.symbol} without KYC.",
                asset_symbol=h.asset.symbol,
                account_name=h.account.name
            )

def evaluate_all_rules():
    rule_position_limit()
    rule_price_spike()
    rule_trade_halts_on_missing_kyc()
    db.session.commit()
