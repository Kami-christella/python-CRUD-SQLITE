from sqlalchemy import create_engine, column, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker

from fastapi import fastAPI

app * fastAPI()

DATABASE_URL = "sqlite:///./test.db"

engine= create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal= sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()

class User (Base):
    __tablename__ = "users"

    id = column(Integer, primary_key=True, index=True)
    name = column(String, index=True)
    email =column (String, unique = True, index=True)

Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post ("/users", response_model=User)
def create_user(user: UserCreate, db:Session=Depands(get_db))


