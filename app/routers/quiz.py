from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.get("/start", response_model=List[schemas.QuizQuestionResponse])
def start_quiz(
    count: int = Query(default=10, gt=0, le=50),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_random_questions(db, count=count)
@router.post("/submit", response_model=schemas.QuizSubmitResponse)
def submit_quiz(
    quiz_data: schemas.QuizSubmit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    score, total_questions = crud.submit_quiz(db, quiz_data.answers, user_id=current_user.id)

    return schemas.QuizSubmitResponse(
        score=score,
        total_questions=total_questions,
        message="Quiz submitted successfully",
    )