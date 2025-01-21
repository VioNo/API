import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import urllib

load_dotenv()

DB_DRIVER = os.getenv("DB_DRIVER")
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION")

print(f"DB_DRIVER: {DB_DRIVER}")
print(f"DB_SERVER: {DB_SERVER}")
print(f"DB_DATABASE: {DB_DATABASE}")
print(f"DB_USERNAME: {DB_USERNAME}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_TRUSTED_CONNECTION: {DB_TRUSTED_CONNECTION}")

if not all([DB_DRIVER, DB_SERVER, DB_DATABASE, DB_USERNAME, DB_TRUSTED_CONNECTION]):
    missing_vars = [var for var in ["DB_DRIVER", "DB_SERVER", "DB_DATABASE", "DB_USERNAME", "DB_TRUSTED_CONNECTION"] if not os.getenv(var)]
    raise ValueError(f"Missing database configuration variables: {', '.join(missing_vars)}")

if DB_TRUSTED_CONNECTION.lower() == 'yes':
    if DB_PASSWORD:
        raise ValueError("DB_PASSWORD should not be set when using trusted connection.")
    params = urllib.parse.quote_plus(
        f"DRIVER={DB_DRIVER};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"Trusted_Connection=yes;"
    )
else:
    if not DB_PASSWORD:
        raise ValueError("DB_PASSWORD is required when not using trusted connection.")
    params = urllib.parse.quote_plus(
        f"DRIVER={DB_DRIVER};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD};"
    )

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
metadata = MetaData()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
