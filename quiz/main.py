import uvicorn

from datetime import datetime
from fastapi import FastAPI
from httpx import get

from models import QuestModel, Base
from schemas import QuestNum
from database import db, engine

GET_QUEST_URL = "https://jservice.io/api/random?"

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_questions(question_num):
    question_list = get(GET_QUEST_URL + f"count={question_num}").json()
    return question_list


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
def generate_quiz(questions_num: QuestNum):
    quest_num = questions_num.questions_num
    try:
        last_id = db.query(QuestModel).order_by(
            QuestModel.id.desc()).first().id
    except AttributeError:
        last_id = 0

    while quest_num > 0 and (last_id + quest_num) <= 221510:
        question_list = get_questions(quest_num)
        for question in question_list:
            question_id = question["id"]
            if not db.query(QuestModel).filter(
                    QuestModel.question_id == question_id).first():
                add_quest(question)
                quest_num -= 1
    if last_id == 0:
        return None
    return db.query(QuestModel).filter(QuestModel.id == last_id).first()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
