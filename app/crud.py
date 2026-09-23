from app.auth_utils import hash_password
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from sqlalchemy import func
from fastapi import HTTPException

def get_questions(
    db: Session,
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
):
    query = select(models.Question)

    if difficulty is not None:
        query = query.where(models.Question.difficulty == difficulty)

    if category is not None:
        query = query.where(models.Question.category == category)

    result = db.execute(query)
    return result.scalars().all()


def get_question_by_id(db: Session, question_id: int):
    query = select(models.Question).where(models.Question.id == question_id)
    result = db.execute(query)
    return result.scalar_one_or_none()


def create_question(db: Session, question_data: schemas.QuestionCreate):
    new_question = models.Question(**question_data.model_dump())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


def update_question(db: Session, question_id: int, question_data: schemas.QuestionUpdate):
    question = get_question_by_id(db, question_id)

    if question is None:
        return None

    # Only update fields that were actually provided (partial update)
    update_data = question_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(question, field, value)

    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: int):
    question = get_question_by_id(db, question_id)

    if question is None:
        return None

    db.delete(question)
    db.commit()
    return question


def get_user_by_email(db: Session, email: str):
    query = select(models.User).where(models.User.email == email)
    result = db.execute(query)
    return result.scalar_one_or_none()


def get_user_by_username(db: Session, username: str):
    query = select(models.User).where(models.User.username == username)
    result = db.execute(query)
    return result.scalar_one_or_none()


def create_user(db: Session, user_data: schemas.UserCreate):
    hashed_password = hash_password(user_data.password)

    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_result(db: Session, result_data: schemas.ResultCreate, user_id: int):
    new_result = models.Result(
        user_id=user_id,
        score=result_data.score,
        total_questions=result_data.total_questions,
    )
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result


def get_results_by_user(db: Session, user_id: int):
    query = select(models.Result).where(models.Result.user_id == user_id)
    result = db.execute(query)
    return result.scalars().all()


def get_result_by_id(db: Session, result_id: int):
    query = select(models.Result).where(models.Result.id == result_id)
    result = db.execute(query)
    return result.scalar_one_or_none()

def get_random_questions(db: Session, count: int):
    query = select(models.Question).order_by(func.random()).limit(count)
    result = db.execute(query)
    return result.scalars().all()

def submit_quiz(db: Session, answers: list[schemas.AnswerSubmit], user_id: int):
    if not answers:
        raise HTTPException(
            status_code=400,
            detail="No answers submitted."
        )

    total_questions = len(answers)
    score = 0

    seen = set()

    for answer in answers:
        if answer.question_id in seen:
            continue

        seen.add(answer.question_id)

        question = get_question_by_id(db, answer.question_id)

        if question is None:
            continue

        correct = question.answer.strip().lower()
        submitted = answer.user_answer.strip().lower()

        if submitted == correct:
            score += 1

    result_data = schemas.ResultCreate(
        score=score,
        total_questions=total_questions
    )

    create_result(
        db,
        result_data,
        user_id=user_id
    )

    return score, total_questions

def get_dashboard_stats(db: Session, user_id: int):
    results = get_results_by_user(db, user_id)

    total_attempts = len(results)

    if total_attempts == 0:
        return {
            "total_attempts": 0,
            "best_score": 0,
            "average_score": 0,
        }

    scores = [result.score for result in results]

    best_score = max(scores)
    average_score = round(sum(scores) / total_attempts, 2)

    return {
        "total_attempts": total_attempts,
        "best_score": best_score,
        "average_score": average_score,
    }