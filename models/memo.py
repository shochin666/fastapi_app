from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from db import Base


class Memo(Base):
    __tablename__ = "memos"
    memo_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)
