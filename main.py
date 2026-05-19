from sqlalchemy import create_engine, Column, Integer, String
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from fastapi import FastAPI, Depends

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── SQLAlchemy model (database table) ──────────────────────
class User(Base):
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True, index=True)
    name  = Column(String, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# ── Pydantic models (API shapes) ───────────────────────────
class UserCreate(BaseModel):
    """What the client sends IN"""
    name: str
    email: str

class UserResponse(BaseModel):
    """What the API sends back OUT"""
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  # allows reading SQLAlchemy objects

# ── Database dependency ────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Route ──────────────────────────────────────────────────
@app.post("/users/", response_model=UserResponse)  # ← UserResponse, not User
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user