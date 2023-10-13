from sqlalchemy import (Column,
                        Integer,
                        String,
                        DateTime)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class QuestModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime)
    added_at = Column(DateTime)
