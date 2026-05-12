import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Core security
    SECRET_KEY = "super-secure-secret-key-change-this"

    # Database (SQLite)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "db", "awareness.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session settings
    SESSION_PERMANENT = False

    # App behavior
    DEBUG = True