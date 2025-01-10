import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

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


if not all([DB_DRIVER, DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_TRUSTED_CONNECTION]):
    missing_vars = [var for var in ["DB_DRIVER", "DB_SERVER", "DB_DATABASE", "DB_USERNAME", "DB_PASSWORD", "DB_TRUSTED_CONNECTION"] if not os.getenv(var)]
    raise ValueError(f"Missing database configuration variables: {', '.join(missing_vars)}")

if DB_TRUSTED_CONNECTION.lower() == 'yes':
    DATABASE_URL = f"mssql+pyodbc://@{DB_SERVER}/{DB_DATABASE}?driver={DB_DRIVER}&Trusted_Connection={DB_TRUSTED_CONNECTION}"
else:
    DATABASE_URL = f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}?driver={DB_DRIVER}"

# Создание движка и сессии
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
