from app import create_app
from models import db, Account, Asset, Holding
from simulate_feed import seed_initial_ticks

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # Accounts
    a1 = Account(name="Alpha Capital", kyc_complete=True)
    a2 = Account(name="Beta Partners", kyc_complete=False)  # triggers KYC alert
    db.session.add_all([a1, a2])
    db.session.commit()

    # Assets
    assets = [
        Asset(symbol="AAPL", asset_class="EQUITY", position_limit=5000, price_limit_pct=5.0),
        Asset(symbol="TSLA", asset_class="EQUITY", position_limit=3000, price_limit_pct=8.0),
        Asset(symbol="US10Y", asset_class="BOND", position_limit=10000, price_limit_pct=2.0),
        Asset(symbol="BTC", asset_class="CRYPTO", position_limit=50, price_limit_pct=10.0),
    ]
    db.session.add_all(assets)
    db.session.commit()

    # Holdings (one will breach limit; one will breach KYC)
    h1 = Holding(account_id=a1.id, asset_id=assets[0].id, quantity=5200)  # > 5000
    h2 = Holding(account_id=a2.id, asset_id=assets[1].id, quantity=100)   # KYC false
    db.session.add_all([h1, h2])
    db.session.commit()

    seed_initial_ticks()
    print("Database initialized with demo data.")
