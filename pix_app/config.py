import os


class Config:
    SECRET_KEY = "dev"
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")
