from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- User Schemas ----------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Question Schemas ----------

class QuestionCreate(BaseModel):
    title: str
    answer: str
    category: str
    difficulty: str


class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None


class QuestionResponse(BaseModel):
    id: int
    title: str
    answer: str
    category: str
    difficulty: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Result Schemas ----------

class ResultCreate(BaseModel):
    score: int
    total_questions: int


class ResultResponse(BaseModel):
    id: int
    user_id: int
    score: int
    total_questions: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Auth / Login Schemas ----------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

# ---------- Quiz Submission Schemas ----------

class AnswerSubmit(BaseModel):
    question_id: int
    user_answer: str


class QuizSubmit(BaseModel):
    answers: list[AnswerSubmit]


class QuizSubmitResponse(BaseModel):
    score: int
    total_questions: int
    message: str

class QuizQuestionResponse(BaseModel):
    id: int
    title: str
    category: str
    difficulty: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DashboardResponse(BaseModel):
    total_attempts: int
    best_score: int
    average_score: float