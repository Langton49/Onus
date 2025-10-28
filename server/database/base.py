from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import server_settings

engine = create_engine(server_settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Create session connected to the database

Base = declarative_base() # Base class for ORM models (SQLAlchemy uses it to map classes to tables)

# Open connection to db for endpoints that depend on it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()