from datetime import datetime
from pydantic import BaseModel


class QuestSchema(BaseModel):
    id: int
    question_id: int
    question: str
    answer: str
    created_at: datetime
    added_at: datetime

    class Config:
        orm_mode = True


class QuestNum(BaseModel):
    questions_num: int
