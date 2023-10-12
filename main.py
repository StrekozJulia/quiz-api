from datetime import datetime
from fastapi import FastAPI
from httpx import get
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import QuestModel, Base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:StrekoPostgres13!@localhost/postgres"
GET_QUEST_URL = "https://jservice.io/api/random?count=1"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


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


Base.metadata.create_all(bind=engine)

app = FastAPI()


def add_quest(response, db=db):
    quiz = QuestModel(question_id=response["id"],
                      question=response["question"],
                      answer=response["answer"],
                      created_at=response["created_at"],
                      added_at=datetime.now())
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz


@app.post("/generate_quiz/")
async def generate_quiz(questions_num: QuestNum):
    quest_num = questions_num.questions_num
    last_quest_id = db.query(QuestModel).order_by(QuestModel.id.desc()).first().id
    while quest_num > 0:
        response = get(GET_QUEST_URL).json()[0]
        question_id = response["id"]
        if not db.query(QuestModel).filter(QuestModel.question_id == question_id).first():
            add_quest(response)
            quest_num -= 1
    return db.query(QuestModel).filter(QuestModel.id == last_quest_id).first()


@app.get("/")
async def view_all():
    return db.query(QuestModel).offset(0).limit(100).all()
