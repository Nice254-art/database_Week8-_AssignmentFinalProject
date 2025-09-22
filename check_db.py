# check_db.py
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

user = os.getenv("DB_USER")
pwd = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset=utf8mb4"
engine = create_engine(url)
with engine.connect() as conn:
    res = conn.execute("SELECT 1").fetchone()
    print("DB response:", res)
