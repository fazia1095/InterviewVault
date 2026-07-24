from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


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