import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///risk.db"   # set to mysql+pymysql://user:pass@host/db
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JOBS_INTERVAL_SECONDS = int(os.environ.get("JOBS_INTERVAL_SECONDS", "5"))  # feed tick
