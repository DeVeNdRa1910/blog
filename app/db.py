from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL=os.getenv("NEON_DB_URI")

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocomit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()