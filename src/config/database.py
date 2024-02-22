from sqlalchemy import engine, create_engine
from typing import Generator
from sqlalchemy.orm import sessionmaker, declarative_base, Session


orm_engine = create_engine("sqlite:///./database.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=True, autocommit=False, bind=orm_engine)
Base = declarative_base()

Base.metadata.create_all(orm_engine)

def init_db():
    Base.metadata.create_all(orm_engine)

async def get_db() -> Generator:
    try:
        db= SessionLocal()
        yield db
    except:
        db.rollback()
    finally:
        db.close_all()