from src.config.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, String


class UserTable(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=False)

    create_at = Column(DateTime, nullable=True, default=datetime.now())
    update_at = Column(DateTime, nullable=True, onupdate=datetime.now())
