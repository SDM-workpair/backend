from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_PORT = 5432
POSTGRES_PASSWORD = "password123"
POSTGRES_USER = "postgres"
POSTGRES_DB = "fastapi"
POSTGRES_HOST = "postgres"
POSTGRES_HOSTNAME = "0.0.0.0"

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@\
{POSTGRES_HOST}:{DATABASE_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
