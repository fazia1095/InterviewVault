from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/", response_model=List[schemas.QuestionResponse])
def read_questions(
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_questions(db, difficulty=difficulty, category=category)


@router.get("/{question_id}", response_model=schemas.QuestionResponse)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = crud.get_question_by_id(db, question_id)

    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    return question


@router.post("/", response_model=schemas.QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(question_data: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db, question_data)


@router.put("/{question_id}", response_model=schemas.QuestionResponse)
def update_question(
    question_id: int,
    question_data: schemas.QuestionUpdate,
    db: Session = Depends(get_db),
):
    updated_question = crud.update_question(db, question_id, question_data)

    if updated_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    return updated_question


@router.delete("/{question_id}", response_model=schemas.QuestionResponse)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    deleted_question = crud.delete_question(db, question_id)

    if deleted_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    return deleted_question