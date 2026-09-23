from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/results", tags=["Results"])


@router.post("/", response_model=schemas.ResultResponse, status_code=status.HTTP_201_CREATED)
def create_result(
    result_data: schemas.ResultCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_result(db, result_data, user_id=current_user.id)


@router.get("/", response_model=List[schemas.ResultResponse])
def read_my_results(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_results_by_user(db, user_id=current_user.id)


@router.get("/{result_id}", response_model=schemas.ResultResponse)
def read_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = crud.get_result_by_id(db, result_id)

    if result is None or result.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")

    return result