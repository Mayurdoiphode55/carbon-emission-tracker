# db.py — SQLAlchemy engine + databases helper
import os
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL not set in .env")

# For direct SQLAlchemy use (alembic expects an engine URL too)
engine = create_engine(DATABASE_URL, future=True)

# synchronous session factory (if needed)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# async Database object (databases library) for async calls
database = Database(DATABASE_URL)

# declarative base for models
Base = declarative_base()
