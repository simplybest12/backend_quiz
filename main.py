from fastapi import FastAPI,HTTPException,status,Depends
import models,database,schemas
from sqlalchemy.orm import Session
from core.config import settings
from database import engine,SessionLocal
from typing import Annotated


get_db = database.get_db


def create_table():
    models.Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_table()
    return app

app=start_application()

db_dependency  = Annotated[Session,Depends(get_db)]

@app.post('/question',status_code=status.HTTP_201_CREATED)

async def createQuestion(question : schemas.QuestionBase , db:db_dependency):
    db_question = models.Questions(question_text = question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(
            choice_text = choice.choice_text, 
            is_correct = choice.is_correct, 
            question_id = db_question.id)
        db.add(db_choice)
    db.commit()
    

@app.get('/questions/{question_Id}')

async def fetch_question(question_Id:int,db:db_dependency):
    question = db.query(models.Questions).filter(models.Questions.id == question_Id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Question not found")
    return question
    
@app.get('/choices/{question_Id}')

async def fetch_choices(question_Id:int,db:db_dependency):
    choices = db.query(models.Choices).filter(models.Choices.question_id == question_Id).all()
    if not choices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Choices not found")
    return choices